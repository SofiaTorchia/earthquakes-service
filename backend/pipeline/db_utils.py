"""
Backend service for retrieving earthquake data from the USGS Earthquake API
and writing it into a Postgres database
"""

import logging
import time
from pathlib import Path
import os
import datetime
import requests
import psycopg
from pydantic.dataclasses import dataclass


initialization_queries_path = Path("backend/pipeline/db_init.sql")
logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)


@dataclass
class Params:
    format: str
    starttime: str
    endtime: str
    limit: int


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


def get_earthquake_data(params: Params, conn: psycopg.Connection) -> None:
    """
    Retrieves earthquake data from the database as a GeoJSON FeatureCollection using
    the provided time window and limit.
    """

    api_params = {
        "format": params.format,
        "starttime": params.starttime,
        "endtime": params.endtime,
        "limit": params.limit,
    }
    response = read_data(api_params)
    logging.info("Retrieved earthquakes data")
    features = response.get("features", [])

    for f in features:
        write_event(f, conn)
    logging.info("Written %d earthquake events", len(features))

    conn.close()
    logging.info("Closed connection to Postgres Database")
