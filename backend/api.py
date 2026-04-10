"""
Backend service for retrieving earthquake data from the USGS Earthquake API.
"""

import logging
import os
from fastapi import FastAPI
import psycopg

conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB", "postgresDB"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "pa"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)

app = FastAPI()


@app.get("/earthquakes")
async def get_earthquakes(format: str, starttime: str, endtime: str, limit: str):
    """
        Endpoint for retrieving earthquake data from database.
        The endpoint accepts query parameters that specify the time window and the
        maximum number of records to return.
        The response is formatted as a GeoJSON FeatureCollection,
        which is compatible with the USGS Earthquake API format.

    Parameters:
        format (str): Output format expected by the USGS API (e.g., "geojson").
        starttime (str): Start of the time window for the earthquake search (ISO 8601 string).
        endtime (str): End of the time window for the earthquake search (ISO 8601 string).
        limit (str):  Maximum number of earthquake records to return.
    Returns
        dict: JSON responses returned by the database.
    """

    earthquake_events = get_earthquake_data(starttime, endtime, limit)
    response = {
        "type": "FeatureCollection",
        "metadata": {"limit": limit},
        "features": [],
    }
    for event in earthquake_events:
        feature = format_geojson_feature(event)
        response["features"].append(feature)

    logging.info("Retrieved earthquakes data")
    return response


def get_earthquake_data(starttime: str, endtime: str, limit: str) -> list[dict]:
    """
    Retrieves earthquake data from the database based on the specified time window and limit.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            select json_agg(row_to_json(t))
            from (
                select * from earthquakes where time >= %s and time <= %s limit %s 
            ) as t
            """,
            (
                starttime,
                endtime,
                limit,
            ),
        )
        return cur.fetchone()[0]


def format_geojson_feature(event: dict) -> dict:
    """Reshapes the earthquake event data into a GeoJSON feature format."""
    feature = {
        "type": "Feature",
        "id": event["id"],
        "properties": {
            "mag": event["magnitude"],
            "time": event["time"],
            "alert": event["alert"],
        },
        "geometry": {
            "type": "Point",
            "coordinates": [event["lon"], event["lat"]],
        },
    }
    return feature
