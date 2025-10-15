import sqlite3
from sqlite3 import Error
from sqlite3 import dbapi2 as sqlite
import csv



# PLEASE DESCRIBE -
# This function creates a connection to the sqlite database by initializing the `conn` variable,
# and then connecting to whatever db_file is specified
# If the connection fails, the error is printed and `None` is returned
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

# PLEASE DESCRIBE -
# This function runs a sql query using an established database connection
# Then it prints the rows resulting from the query input
# Lastly, it returns the number of rows returned from the query
def db_query(conn, query):
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        print(row)

    return len(rows)

# PLEASE DESCRIBE -
# This is a query that first selects all from a specific table, and then returns only the column names of that table
def db_getinfo(conn, tbl_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + tbl_name)
    column_name_list = [tuple[0] for tuple in cur.description]

    return column_name_list

# PLEASE DESCRIBE -
# This is a function that ultimately loads data from a csv into a given table
def loadcsv(conn, file_name, tbl_name):
    # PLEASE DESCRIBE -
    # It opens the CSV and reads its header to determine column names, then constructs a SQL INSERT statement.
    # The insert_sql variable is a command that will later push the csv's data into the tbl_name, the print statement shows us what that command will look like
    csv_file = open(file_name)
    csv_reader = csv.DictReader(csv_file)
    insert_sql = 'INSERT INTO ' + tbl_name + ' (' + ','.join(csv_reader.fieldnames) + ') VALUES (' + ','.join(['?'] * len(csv_reader.fieldnames))+ ')'
    print(insert_sql)
    # PLEASE DESCRIBE -
    # The CSV rows are collected into a list of lists (`values`) for bulk insertion.
    values = []
    for datarow in csv_reader:
        row_values = []
        for field in csv_reader.fieldnames:
            row_values.append(datarow[field])
        values.append(row_values)

    # This section is an execution of the insert_sql command we created earlier, and commits the changes

    conn.executemany(insert_sql, values)
    conn.commit()
