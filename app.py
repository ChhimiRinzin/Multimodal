import os
import sqlite3
from decimal import Decimal

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text

st.set_page_config(page_title="Audit Recovery Dashboard", page_icon="💰", layout="centered")
st.title("Audit Recovery Dashboard")
st.caption("Read-only prototype • Total recovered amount")

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///demo_recoveries.db")
TABLE_NAME = os.getenv("RECOVERY_TABLE", "recoveries")
AMOUNT_COLUMN = os.getenv("RECOVERED_AMOUNT_COLUMN", "recovered_amount")
STATUS_COLUMN = os.getenv("RECOVERY_STATUS_COLUMN", "status")

# Identifiers are not SQL parameters; restrict them to safe, simple names.
def check_identifier(value: str) -> str:
    if not value or not (value[0].isalpha() or value[0] == "_") or not all(c.isalnum() or c == "_" for c in value):
        raise ValueError("Table and column names must contain only letters, numbers or underscores.")
    return value

@st.cache_data(ttl=60)
def get_total(db_url: str, table: str, amount: str, status: str) -> Decimal:
    table, amount, status = map(check_identifier, (table, amount, status))
    engine = create_engine(db_url)
    query = text(f"SELECT {amount} FROM {table} WHERE {status} = :status")
    with engine.connect() as conn:
        amounts = conn.execute(query, {"status": "Recovered"}).scalars().all()
    # Convert from string for exact decimal arithmetic; no double counting from joins.
    return sum((Decimal(str(v)) for v in amounts if v is not None), Decimal("0"))

try:
    total = get_total(DATABASE_URL, TABLE_NAME, AMOUNT_COLUMN, STATUS_COLUMN)
    st.metric("Total Recovered", f"Nu. {total:,.2f}")
    st.caption("Sum of recovered_amount for records with status = 'Recovered'.")
    if st.button("Refresh"):
        get_total.clear()
        st.rerun()
except Exception:
    st.error("Unable to load recovery data. Check the database connection and configured table/column names.")
    st.info("For a real database, ask your database administrator for a read-only connection and a vetted recovery summary view.")
