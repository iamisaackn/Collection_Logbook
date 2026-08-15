# db.py – Database Connection Handler
import psycopg2
import psycopg2.extras
from config import DB_CONFIG


def get_connection():
    """Return a live psycopg2 connection."""
    return psycopg2.connect(**DB_CONFIG)


def run_query(sql: str, params: dict = None) -> list[dict]:
    """
    Execute a SELECT query and return rows as a list of dicts.
    Uses RealDictCursor so column names are preserved.
    """
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params or {})
            return [dict(row) for row in cur.fetchall()]


def run_write(sql: str, params: dict = None) -> int:
    """
    Execute an INSERT / UPDATE and return the number of affected rows.
    Commits automatically.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params or {})
            conn.commit()
            return cur.rowcount
