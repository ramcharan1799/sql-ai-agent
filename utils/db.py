import sqlite3
import pandas as pd

DB_PATH = "company.db"

def get_schema() -> str:
    """Returns the full schema as a string for the LLM prompt."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cur.fetchall()]
    schema_parts = []
    for table in tables:
        cur.execute(f"PRAGMA table_info({table})")
        cols = cur.fetchall()
        col_defs = ", ".join([f"{c[1]} {c[2]}" for c in cols])
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        schema_parts.append(f"Table: {table} ({count} rows)\nColumns: {col_defs}")
    conn.close()
    return "\n\n".join(schema_parts)


def run_query(sql: str) -> tuple[pd.DataFrame, str]:
    """
    Executes a SQL query safely (read-only).
    Returns (dataframe, error_message).
    error_message is empty string if successful.
    """
    sql_upper = sql.strip().upper()
    if not sql_upper.startswith("SELECT"):
        return pd.DataFrame(), "Only SELECT queries are allowed."
    forbidden = ["DROP", "DELETE", "INSERT", "UPDATE", "ALTER", "CREATE"]
    for word in forbidden:
        if word in sql_upper:
            return pd.DataFrame(), f"Forbidden keyword: {word}"
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(sql, conn)
        conn.close()
        return df, ""
    except Exception as e:
        return pd.DataFrame(), str(e)


def sample_data() -> dict:
    """Returns 3 sample rows from each table for context."""
    conn = sqlite3.connect(DB_PATH)
    samples = {}
    for table in ["departments", "employees", "sales"]:
        df = pd.read_sql_query(f"SELECT * FROM {table} LIMIT 3", conn)
        samples[table] = df.to_string(index=False)
    conn.close()
    return samples
