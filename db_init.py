import psycopg
import os
import logging
from pathlib import Path

conn = psycopg.connect(
    dbname=os.getenv("POSTGRES_DB", "postgresDB"),
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "pa"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    port=os.getenv("POSTGRES_PORT", "5432")
)

initialization_queries_path = Path("db_init.sql")

logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s - %(message)s - %(asctime)s'
)

def initialize_db() -> None:
    with open(initialization_queries_path, "r") as f:
        query = f.read()
    with conn.cursor() as cur:
        cur.execute(query)
    conn.commit()
    conn.close()


if __name__ == "__main__":
    initialize_db()
    logging.info('Initialized Postgres Database')
