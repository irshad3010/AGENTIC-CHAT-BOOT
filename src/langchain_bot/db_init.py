
import sqlite3
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database and SQL seed file paths
DB_PATH = PROJECT_ROOT / "ecommerce.db"
SQL_SEED_PATH = PROJECT_ROOT / "ecommerce_setup.sql"


def init_database():
    """Initialize SQLite database using SQL seed file."""

    # Ensure database parent directory exists
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Check SQL seed file
    if not SQL_SEED_PATH.exists():
        raise FileNotFoundError(
            f"SQL seed file not found: {SQL_SEED_PATH}"
        )

    # Read SQL file
    sql_script = SQL_SEED_PATH.read_text(
        encoding="utf-8"
    )

    # Execute SQL script
    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(sql_script)
        conn.commit()

    return DB_PATH


def main():
    database_path = init_database()

    print("Database initialized successfully!")
    print(f"Database location: {database_path}")


if __name__ == "__main__":
    main()

