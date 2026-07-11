import sqlite3
import os

conn = sqlite3.connect("industrial_brain.db")
c = conn.cursor()
c.execute("SELECT id, knowledge_status FROM documents")
rows = c.fetchall()
for r in rows:
    print(r)
