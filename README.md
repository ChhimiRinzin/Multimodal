# Audit Recovery Dashboard — minimum prototype

Shows one KPI: **Total Recovered**. The bundled SQLite database contains *fictional* data; it is not connected to RAA.

## Run

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python create_demo_db.py
streamlit run app.py
```

Open the local URL Streamlit prints (typically http://localhost:8501). Expected total: **Nu. 80,000.00**.

## Connect to an existing SQL database

Set `DATABASE_URL`, `RECOVERY_TABLE`, `RECOVERED_AMOUNT_COLUMN`, and `RECOVERY_STATUS_COLUMN` in the process environment before running. Example (SQLite demo):

```bash
export DATABASE_URL='sqlite:///demo_recoveries.db'
export RECOVERY_TABLE='recoveries'
export RECOVERED_AMOUNT_COLUMN='recovered_amount'
export RECOVERY_STATUS_COLUMN='status'
streamlit run app.py
```

For MySQL, SQL Server, Oracle, or PostgreSQL, install the corresponding SQLAlchemy driver and use its connection URL. Ask your DBA to provide a **read-only user and preferably an approved view** exposing one row per actual recovery entry, with the correct amount and status. Your schema and definition of 'recovered' may be different: adjust the validated query before using official figures. No receipts or images are accessed in this initial version.

**Security:** Keep credentials in environment variables or secrets storage, never source code. Do not expose this prototype to the public internet; enforce organizational authentication and authorization before production. Avoid logging private records.
