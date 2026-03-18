from fastapi import FastAPI
import logging
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s - %(asctime)s'
)

app = FastAPI()

@app.get("/earthquakes")
async def get_earthquakes(format: str, starttime: str, endtime: str, limit: str):
    params = {
        'format': format, 
        'starttime': starttime, 
        'endtime' : endtime, 
        'limit': limit
    }
    response = requests.get(
        'https://earthquake.usgs.gov/fdsnws/event/1/query?', 
        params=params
    )
    logging.info(f'Retrieved earthquakes data')
    return response.json()
