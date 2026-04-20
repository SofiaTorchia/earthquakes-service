"""
This module updates Postgres db with earthquake data from the last 7 days.
It is intended to be run as a cron job every day.
"""

from datetime import date, timedelta
import yaml
import logging
import db_utils
import datetime
from pydantic.dataclasses import dataclass


@dataclass
class Params:
    format: str
    starttime: datetime.datetime
    endtime: datetime.datetime
    limit: int


if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO, format="%(levelname)s - %(message)s - %(asctime)s"
    )

    conn = db_utils.start_db_connection()
    logging.info("Started connection to Postgres Database")

    with open("backend/pipeline/params.yaml", "r") as f:
        params = yaml.safe_load(f)

    endtime = date.today().strftime("%Y-%m-%d")
    delta_days = params["update"]["delta_days"]
    starttime = (date.today() - timedelta(days=delta_days)).strftime("%Y-%m-%d")
    params = Params(
        format=params["update"]["format"],
        starttime=starttime,
        endtime=endtime,
        limit=params["update"]["limit"],
    )
    db_utils.get_earthquake_data(params, conn)
