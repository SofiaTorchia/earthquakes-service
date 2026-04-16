"""
Backend service for retrieving earthquake data from the USGS Earthquake API
and writing it into a Postgres database
"""

import logging
import time
from pathlib import Path
import os
import requests
import psycopg


logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)
conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB", "postgresDB"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "pa"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)
initialization_queries_path = Path("backend/db_init.sql")


def initialize_db() -> None:
    """
    Initializes earthquakes Postgres database
    """
    with open(initialization_queries_path, "r") as f:
        query = f.read()
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()


def read_data(params: dict) -> dict:
    """
    Retrieves data from USGS API
    """
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query?", params=params, timeout=100
    )
    logging.info("Retrieved earthquakes data")
    return response.json()


def write_event(feature: dict) -> None:
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


def close_connection() -> None:
    """
    Closes connection to Postgres database
    """
    conn.close()
