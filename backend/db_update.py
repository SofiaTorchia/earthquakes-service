"""
This module updates Postgres db with earthquake data from the last 7 days.
It is intended to be run as a cron job every day.
"""

import logging
from datetime import date, timedelta
import db_utils

endtime = date.today().strftime("%d-%m-%Y")
starttime = (date.today() - timedelta(days=7)).strftime("%d-%m-%Y")
params = {
    "format": "geojson",
    "starttime": starttime,
    "endtime": endtime,
    "limit": 1000,
}

response = db_utils.read_data(params)
features = response.get("features", [])

for f in features:
    db_utils.write_event(f)
logging.info("Written earthquake events")

db_utils.close_connection()
logging.info("Closed connection to Postgres Database")
