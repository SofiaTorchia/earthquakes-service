"""
This script initializes the Postgres database by creating the earthquakes table
and populating it with earthquake data from the USGS API for the last 2 years.
"""

import db_utils

if __name__ == "__main__":

    conn = db_utils.start_db_connection()

    db_utils.initialize_db(conn)
    config = db_utils.load_config()
    window_config = config.init
    db_utils.get_earthquake_data(window_config, conn)
