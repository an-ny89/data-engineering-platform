import os
import logging
import psycopg
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Database configuration from environment variables
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD")
}


def extract_data(query):

    conn = None

    try:
        logger.info("Starting data extraction")

        conn = psycopg.connect(**DB_CONFIG)

        with conn.cursor() as cur:
            cur.execute(query)

            rows = cur.fetchall()
            columns = [column[0] for column in cur.description]

            df = pd.DataFrame(rows, columns=columns)

        logger.info("Extraction successful. Records extracted: %s", len(df))

        return df

    except Exception:
        logger.exception("Data extraction failed")
        raise

    finally:
        if conn is not None:
            conn.close()