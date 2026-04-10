"""
Sreamlit frontend for earthquake-service app
"""

import time
import streamlit as st
import pandas as pd
import requests

API_URL = "http://127.0.0.1:8000/earthquakes"


def choose_date():
    """
    Display two Streamlit date selectors and return the chosen
    start and end dates.
    """
    col1, col2 = st.columns(2)
    with col1:
        start = str(st.date_input("Start date"))
    with col2:
        end = str(st.date_input("End date"))
    return start, end


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
    # times = [
    #    time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(f["properties"]["time"] / 1000))
    #    for f in features
    # ]
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
        r = requests.get(API_URL, payload, timeout=10)
        return r.json()
    return {}


def main():
    """
    Render the main interface of the Earthquake Explorer Streamlit app.
    """
    st.title("Earthquakes")
    st.write(
        ""
        "Select starting and ending dates and view up to 10 thousands earthquakes "
        "occurred during this time span. Choose whether to focus on a limited area "
        "or to have a global perspective."
    )
    start, end = choose_date()

    if st.button("Display Data"):
        payload = {
            "format": "geojson",
            "starttime": start,
            "endtime": end,
            "limit": "100",
        }
        df = parse_geojson_features(fetch_earthquake_data(payload))

        if df.empty:
            st.write("No earthquakes occurred.")
        else:
            st.map(df)
            st.write("Real-time data taken from https://earthquake.usgs.gov/")
    else:
        return
    return


main()
