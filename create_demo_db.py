import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("demo_recoveries.db")
with sqlite3.connect(DB) as conn:
    conn.execute("DROP TABLE IF EXISTS recoveries")
    conn.execute("CREATE TABLE recoveries (id INTEGER PRIMARY KEY, agency TEXT, recovered_amount TEXT, status TEXT)")
    conn.executemany("INSERT INTO recoveries (agency, recovered_amount, status) VALUES (?, ?, ?)", [
        ("Agency A", "25000.00", "Recovered"),
        ("Agency B", "40000.00", "Recovered"),
        ("Agency C", "15000.00", "Recovered"),
        ("Agency D", "30000.00", "Outstanding"),
    ])
print("Created demo_recoveries.db; expected recovered total: Nu. 80,000.00")
