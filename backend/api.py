from fastapi import FastAPI
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s - %(asctime)s'
)

app = FastAPI()

@app.get("earthquakes/format={format}&starttime={start}&endtime={end}&limit={limit}")
async def get_earthquakes(format: str, start: str, end: str, limit: int):
    params = {
        'format': format, 
        'starttime': start, 
        'endtime' : end, 
        'limit': limit
    }
    response = requests.get(
        'https://earthquake.usgs.gov/fdsnws/event/1/query?', 
        params=params
    )
    logging.info(f'Retrieved earthquakes data')
    return response.json()
