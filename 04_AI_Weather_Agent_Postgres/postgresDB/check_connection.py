import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv


def check_connection() -> bool:
    env_file = Path(__file__).resolve().parent.parent / ".env"
    load_dotenv(env_file)

    database_uri = os.getenv("SUPABASE_DB_URI")
    if not database_uri:
        print("Database connection failed: SUPABASE_DB_URI is not set.")
        return False

    try:
        with psycopg.connect(database_uri, connect_timeout=10) as connection:
            connection.execute("SELECT 1")
    except psycopg.Error as error:
        print(f"Database connection failed ({type(error).__name__}).")
        return False

    print("Database connection successful.")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if check_connection() else 1)
