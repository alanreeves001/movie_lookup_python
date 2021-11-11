import sqlite3
import os

def CreateDatabaseFile(db_name):
    sqlite3.connect(db_name)

def ConnectToDatabase(db_file):
    # checks to see if the file exists. If not, return error
    if os.path.isfile(db_file):
        print("Found database file")
        return sqlite3.connect(db_file)
    else:
        print ("ERROR: database does not exist")
        return False

def CloseDatabaseConnection(conn):
    conn.close()

def ExecuteQuery(conn, query, query_parameters):

    c = conn.cursor()
    c.execute(query, query_parameters)
    conn.commit()
    return c
