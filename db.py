import sqlite3

def CreateDatabase(): #creates the database file. May not be needed since connect should connect to the file or create a new file
    pass

def CheckForDatabaseFile(db_name):
    pass

def ConnectToDatabase(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def CreateMovieDatabase():
    pass

def CreateResultDatabase():
    pass

def CloseDatabaseConnection(conn):
    conn.close()

def CommitToDB(conn):
    conn.commit()

def ExecuteQuery(conn, query, query_parameters):
    c = conn.cursor()
    c.execute(query, parameters)

# cursor.execute("SELECT admin FROM users WHERE username = %(username)s", {'username': username});





# on opening, check for database file.
#   if no file, create database with appropriate columns
#   If file, create connection





# c.execute("""CREATE TABLE employees (
#             first text,
#             last text,
#             pay integer
#             """)



#  c.execute("INSERT INTO employees VALUES ('Adam', 'Smith', 50000)")

c.execute("SELECT * FROM employees WHERE last like '%S%'")

print(c.fetchone())

