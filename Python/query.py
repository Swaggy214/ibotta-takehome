import sqlite3
from db_utils import db_query, create_connection

# Connect to the database
conn = create_connection("database/ibotta.db")

# modify sql variable to query command you want to run
sql = "INSERT QUERY HERE;"
num_rows = db_query(conn, sql)

print(f"Returned {num_rows} rows")

conn.close()
