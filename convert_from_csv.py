#! python 3
# convert_from_csv.py

from db import CloseDatabaseConnection,  \
                ConnectToDatabase,       \
                CreateDatabaseFile,      \
                ExecuteQuery,           \
                CloseDatabaseConnection

import csv
import datetime

def CreateMoviesDatabase(conn):
    print("Creating Movie database...")
    query = """CREATE TABLE movies (
                    movie_id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL,
                    date_added TEXT DEFAULT "", 
                    on_hold INTEGER DEFAULT 0, 
                    viewed INTEGER DEFAULT 0, 
                    delflag INTEGER DEFAULT 0)
            """
    return ExecuteQuery(conn, query, "") #(conn, query, query_parameters)


def CreateResultsDatabase(conn):
    print ("creating results database...")
    query = """CREATE TABLE results (
                    result_id INTEGER PRIMARY KEY,
                    movie_id INTEGER,
                    result_title TEXT NOT NULL,
                    format TEXT,
                    release_date text,
                    url TEXT NOT NULL,
                    no_match INTEGER,
                    delflag INTEGER)
            """
    return ExecuteQuery(conn, query, "") #(conn, query, query_parameters)

db_file = "./movies.db"
source_file = "movies.csv"

conn = ConnectToDatabase(db_file)

# if there is no database file, create the database file and necessary databases
if not conn:
    CreateDatabaseFile(db_file)
    conn = ConnectToDatabase(db_file)
    CreateMoviesDatabase(conn)
    CreateResultsDatabase(conn)

# ------------ All necessary databases should be setup 

source = open(source_file)

data_list = list(csv.reader(source))
now = datetime.datetime.now()

for row in data_list:
    # print(row[0])
    on_hold = 0

    # Skips rows with "DVD--" in the title (separators)
    if row[0].find("DVD--") >= 0:
        continue

    # Marks any movies with "---" before the title as on_hold (and removes the "---" from the title)
    if row[0].find("---") >= 0:
        row[0] = row[0][3:]
        on_hold = 1
    
    query = """INSERT INTO movies (title, date_added, on_hold) 
                           VALUES (:title, 
                                   :date_added,
                                   :on_hold)
            """
    query_parameters = {'title': row[0].title(),
                        'date_added': now.strftime("%Y-%m-%d"),
                        'on_hold': on_hold
                        }
    # print(query)
    # print(query_parameters)

    ExecuteQuery(conn, query, query_parameters)    

CloseDatabaseConnection(conn)