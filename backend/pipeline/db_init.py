"""
This script initializes the Postgres database by creating the earthquakes table
and populating it with earthquake data from the USGS API for the last 2 years.
"""

import logging
import yaml
import db_utils

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)

conn = db_utils.start_db_connection()
logging.info("Started connection to Postgres Database")

db_utils.initialize_db(conn)
logging.info("Initialized Postgres Database")

with open("backend/pipeline/db_init.yaml", "r") as f:
    params = yaml.safe_load(f)
db_utils.get_earthquake_data(params["params"], conn)
make
