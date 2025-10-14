import sqlite3
from db_utils import db_query, create_connection

# Connect to the database
conn = create_connection("database/ibotta.db")

# Example query
sql = "INSERT QUERY HERE;"
num_rows = db_query(conn, sql)

print(f"Returned {num_rows} rows")

conn.close()
