"""
This module updates Postgres db with earthquake data from the last 7 days.
It is intended to be run as a cron job every day.
"""

import db_utils

if __name__ == "__main__":
    conn = db_utils.start_db_connection()
    config = db_utils.load_config()
    window_config = db_utils.get_update_config(config)
    db_utils.get_earthquake_data(window_config, conn)
