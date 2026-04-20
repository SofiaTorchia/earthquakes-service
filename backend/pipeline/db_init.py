"""
This script initializes the Postgres database by creating the earthquakes table
and populating it with earthquake data from the USGS API for the last 2 years.
"""

import logging
import yaml
import db_utils

# import datetime
from db_utils import Params

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
    )

    conn = db_utils.start_db_connection()
    logging.info("Started connection to Postgres Database")

    db_utils.initialize_db(conn)
    logging.info("Initialized Postgres Database")

    with open("backend/pipeline/params.yaml", "r", encoding="utf-8") as f:
        params = yaml.safe_load(f)

    init_params = params["init"]
    # init_params["starttime"] = datetime.datetime.strptime(init_params["starttime"], "%m-%d-%Y")
    # init_params["endtime"] = datetime.datetime.strptime(init_params["endtime"], "%m-%d-%Y")

    params_obj = Params(**init_params)
    db_utils.get_earthquake_data(params_obj, conn)
