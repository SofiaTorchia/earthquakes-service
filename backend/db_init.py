import db_utils
import logging

db_utils.initialize_db()
logging.info("Initialized Postgres Database")

params = {
    "format": "geojson",
    "starttime": "01-01-2024",
    "endtime": "01-01-2026",
    "limit": 1000,
}

response = db_utils.read_data(params)
features = response.get("features", [])

for f in features:
    db_utils.write_event(f)
logging.info("Written eartquake events")

db_utils.close_connection()
logging.info("Closed connection to Postgres Database")
