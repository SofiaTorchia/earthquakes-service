"""
This module updates Postgres db with earthquake data from the last 7 days.
It is intended to be run as a cron job every day.
"""

from datetime import date, timedelta
import logging
import yaml
import db_utils

logging.basicConfig(
    level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
)

conn = db_utils.start_db_connection()
logging.info("Started connection to Postgres Database")

with open("backend/pipeline/db_update.yaml", "r") as f:
    params = yaml.safe_load(f)

endtime = date.today().strftime("%d-%m-%Y")
delta_days = params["params"]["delta_days"]
starttime = (date.today() - timedelta(days=delta_days)).strftime("%d-%m-%Y")
params = {
    "format": params["params"]["format"],
    "starttime": starttime,
    "endtime": endtime,
    "limit": params["params"]["limit"],
}
db_utils.get_earthquake_data(params, conn)
