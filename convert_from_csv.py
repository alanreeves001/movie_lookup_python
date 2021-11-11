#! python 3
# convert_from_csv.py

from db import CloseDatabaseConnection,  \
                ConnectToDatabase,       \
                CreateDatabaseFile,      \
                ExecuteQuery,           \
                CloseDatabaseConnection

from setup import CreateMoviesDatabase, \
                  CreateResultsDatabase

import csv
import datetime

def main():

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


if __name__ == "__main__":
    main()
