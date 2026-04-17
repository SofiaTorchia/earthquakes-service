"""
Backend service for retrieving earthquake data from the USGS Earthquake API.
"""

import datetime
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
async def get_earthquakes(
    starttime: datetime.datetime, endtime: datetime.datetime, limit: int
):
    """
    Endpoint for retrieving earthquake data from database.
    The endpoint accepts query parameters that specify the time window and the
    maximum number of records to return.
    The response is formatted as a GeoJSON FeatureCollection,
    which is compatible with the USGS Earthquake API format.

    Parameters:
        starttime (str): Start of the time window for the earthquake search (ISO 8601 string).
        endtime (str): End of the time window for the earthquake search (ISO 8601 string).
        limit (str):  Maximum number of earthquake records to return.
    Returns
        dict: JSON responses returned by the database.
    """

    earthquake_events = get_earthquake_data(starttime, endtime, limit)
    logging.info("Retrieved earthquakes data")
    return earthquake_events


def get_earthquake_data(
    starttime: datetime.datetime, endtime: datetime.datetime, limit: int
) -> dict:
    """
    Retrieves earthquake data from the database as a GeoJSON FeatureCollection.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT json_build_object(
                'type', 'FeatureCollection',
                'features', coalesce(json_agg(
                    json_build_object(
                        'type', 'Feature',
                        'id', id,
                        'geometry', ST_AsGeoJSON(
                            ST_SetSRID(ST_MakePoint(lon, lat), 4326)
                        )::json,
                        'properties', json_build_object(
                            'magnitude', magnitude,
                            'time', time,
                            'alert', alert
                        )
                    )
                ), '[]'::json)
            ) AS geojson
            FROM earthquakes
            WHERE time >= %s AND time <= %s
            LIMIT %s;
            """,
            (starttime, endtime, limit),
        )

        result = cur.fetchone()[0]
        return result
