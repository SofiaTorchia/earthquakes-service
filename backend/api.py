"""
Backend service for retrieving earthquake data from the USGS Earthquake API.
"""

import logging
from fastapi import FastAPI
import requests

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)

app = FastAPI()


@app.get("/earthquakes")
async def get_earthquakes(format: str, starttime: str, endtime: str, limit: str):
    """
    This endpoint acts as a proxy between the client and the USGS FDSN Event Web Service.
    It forwards the provided query parameters to the external API and returns the resulting
    JSON payload.

    Parameters:
        format (str): Output format expected by the USGS API (e.g., "geojson").
        starttime (str): Start of the time window for the earthquake search (ISO 8601 string).
        endtime (str): End of the time window for the earthquake search (ISO 8601 string).
        limit (str):  Maximum number of earthquake records to return.
    Returns
        dict: JSON response returned by the USGS Earthquake API.
    """
    params = {
        "format": format,
        "starttime": starttime,
        "endtime": endtime,
        "limit": limit,
    }
    response = requests.get(
        "https://earthquake.usgs.gov/fdsnws/event/1/query?", params=params, timeout=10
    )
    logging.info("Retrieved earthquakes data")
    return response.json()
