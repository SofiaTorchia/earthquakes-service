"""
Backend service for retrieving earthquake data from the USGS Earthquake API
and writing it into a Postgres database
"""

from datetime import date, timedelta
import logging
import time
import yaml
from pathlib import Path
import os
import requests
import psycopg
from pydantic import BaseModel


initialization_queries_path = Path("backend/pipeline/db_init.sql")
config_path = Path("backend/pipeline/config.yaml")
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)


class TimeRangeConfig(BaseModel):
    format: str
    delta_days: int
    limit: int


class WindowConfig(BaseModel):
    format: str
    starttime: str
    endtime: str
    limit: int


class Config(BaseModel):
    update: TimeRangeConfig
    init: WindowConfig


def start_db_connection() -> psycopg.Connection:
    """
    Starts connection to Postgres database
    """
    conn = psycopg.connect(
        dbname=os.getenv("POSTGRES_DB", "postgresDB"),
        user=os.getenv("POSTGRES_USER", "postgres"),
        password=os.getenv("POSTGRES_PASSWORD", "pa"),
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=os.getenv("POSTGRES_PORT", "5432"),
    )
    logging.info("Started connection to Postgres Database")
    return conn


def initialize_db(conn: psycopg.Connection) -> None:
    """
    Initializes earthquakes Postgres database
    """
    with open(initialization_queries_path, "r", encoding="utf-8") as f:
        query = f.read()
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
    logging.info("Initialized Postgres Database")


def read_data(params: dict) -> dict:
    """
    Retrieves data from USGS API
    """
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query?", params=params, timeout=3000
    )
    return response.json()


def write_event(feature: dict, conn: psycopg.Connection) -> None:
    """
    Writes earthquakes event on a db
    """
    lon = feature["geometry"]["coordinates"][0]
    lat = feature["geometry"]["coordinates"][1]
    alert = feature["properties"]["alert"]
    mag = feature["properties"]["mag"]
    t = time.strftime(
        "%Y-%m-%d %H:%M:%S", time.gmtime(feature["properties"]["time"] / 1000)
    )
    quake_id = feature["id"]

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO earthquakes (id, lat, lon, magnitude, time, alert)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                lat = EXCLUDED.lat,
                lon = EXCLUDED.lon,
                magnitude = EXCLUDED.magnitude,
                time = EXCLUDED.time,
                alert = EXCLUDED.alert;
            """,
            (quake_id, lat, lon, mag, t, alert),
        )
    conn.commit()


def get_earthquake_data(window_config: WindowConfig, conn: psycopg.Connection) -> None:
    """
    Retrieves earthquake data from the database as a GeoJSON FeatureCollection using
    the provided time window and limit.
    """

    api_params = {
        "format": window_config.format,
        "starttime": window_config.starttime,
        "endtime": window_config.endtime,
        "limit": window_config.limit,
    }
    response = read_data(api_params)
    logging.info("Retrieved earthquakes data")
    features = response.get("features", [])

    for f in features:
        write_event(f, conn)
    logging.info("Written %d earthquake events", len(features))

    conn.close()
    logging.info("Closed connection to Postgres Database")


def load_config() -> Config:
    """
    Loads configuration from a YAML file and returns a Config object.
    """
    with open(config_path, "r", encoding="utf-8") as f:
        input_config = yaml.safe_load(f)
    config = Config(
        update=TimeRangeConfig(**input_config["update"]),
        init=WindowConfig(**input_config["init"]),
    )
    return config


def get_update_config(config: Config) -> WindowConfig:
    """
    Extracts the update configuration from the Config object and returns a WindowConfig object.
    """
    return WindowConfig(
        format=config.update.format,
        starttime=(date.today() - timedelta(days=config.update.delta_days)).strftime(
            "%Y-%m-%d"
        ),
        endtime=date.today().strftime("%Y-%m-%d"),
        limit=config.update.limit,
    )
