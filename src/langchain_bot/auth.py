
import sqlite3
from pathlib import Path
from typing import TypedDict, Optional


class UserRecord(TypedDict):
    email: str
    full_name: str
    role: str


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "ecommerce.db"


def authenticate_user(
    email: str,
    password: str,
    role: Optional[str] = None
) -> Optional[UserRecord]:

    query = """
        SELECT email, full_name, role
        FROM users
        WHERE email = ? AND password = ?
    """

    params = [email, password]

    if role:
        query += " AND role = ?"
        params.append(role)

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row

        user = conn.execute(
            query,
            params
        ).fetchone()

    if user is None:
        return None

    return {
        "email": user["email"],
        "full_name": user["full_name"],
        "role": user["role"]
    }
