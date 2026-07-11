import sqlite3
import os

conn = sqlite3.connect("industrial_brain.db")
c = conn.cursor()
c.execute("SELECT id, processing_status, knowledge_status, graph_status FROM documents WHERE id='bdeb5607-1079-4129-8758-554d3c828622'")
print(c.fetchone())
