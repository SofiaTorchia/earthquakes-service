from fastapi import FastAPI
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s - %(asctime)s'
)

app = FastAPI()

@app.get("/{start}/{end}")
async def user_details(start: str, end: str):
    params = {
        'format': 'geojson', 
        'starttime': start, 
        'endtime' : end, 
        'limit': 10
    } 
    response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?', params=params)
    logging.info(f'Retrieved earthquakes data')
    return response.json()