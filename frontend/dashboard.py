"""
Sreamlit frontend for earthquake-service app
"""

from datetime import datetime

import streamlit as st
import pandas as pd
import requests

API_URL = "http://earthquakes-api.railway.internal:8080/earthquakes"
#API_URL = "http://localhost:8000/earthquakes"
MIN_DATE = datetime(2026, 1, 1)
MAX_DATE = "today"
LIMIT = 20000



@st.cache_data()
def parse_geojson_features(data):
    """
    Convert a GeoJSON-like dictionary containing feature objects
    into a pandas DataFrame.
    """
    features = data.get("features", [])
    if not features:
        return pd.DataFrame()
    longitudes = [f["geometry"]["coordinates"][0] for f in features]
    latitudes = [f["geometry"]["coordinates"][1] for f in features]
    alerts = [f["properties"].get("alert") for f in features]
    magnitudes = [f["properties"].get("mag") for f in features]
    times = [f["properties"]["time"] for f in features]
    df = pd.DataFrame(
        {
            "lat": latitudes,
            "lon": longitudes,
            "magnitude": magnitudes,
            "time": times,
            "alert": alerts,
        }
    )
    return df


@st.cache_data
def fetch_earthquake_data(payload):
    """
    Query the USGS Earthquake API using the provided request parameters.
    """
    if payload:
        r = requests.get(API_URL, payload, timeout=3000)
        return r.json()
    return {}


def main():
    """
    Render the main interface of the Earthquake Explorer Streamlit app.
    """
    st.title("Earthquakes")
    st.write(
        ""
        "Select starting and ending dates and view up to 20 thousands earthquakes "
        "occurred since Jan 1st, 2026 until today."
    )
    range = st.date_input("", (MIN_DATE, MAX_DATE), min_value=MIN_DATE, max_value=MAX_DATE)

    if st.button("Display Data"):
        payload = {
            "starttime": range[0].strftime("%Y-%m-%d"),
            "endtime": range[1].strftime("%Y-%m-%d"),
            "limit": LIMIT,
        }
        df = parse_geojson_features(fetch_earthquake_data(payload))
        if df.empty:
            st.write("No earthquakes occurred.")
        else:
            st.map(df)
            st.write("Data source: https://earthquake.usgs.gov/")
    else:
        return
    return


main()
