#! python 3
# setup.py

from db import CloseDatabaseConnection,  \
                ConnectToDatabase,       \
                CreateDatabaseFile,      \
                ExecuteQuery,            \
                CloseDatabaseConnection


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


def CreateSettingsDatabase(conn):
    print ("creating settings database...")
    query = """CREATE TABLE settings (
                    setting_id INTEGER PRIMARY KEY,
                    user_id INTEGER DEFAULT 0,
                    setting_name TEXT NOT NULL,
                    setting_value TEXT NOT NULL,
                    delflag INTEGER DEFAULT 0)
            """
    return ExecuteQuery(conn, query, "") #(conn, query, query_parameters)

def InitializeSettings(conn):
    print("Initializing settings table...")
    AddSetting(conn, "SEARCH_URL", "https://mobi.ent.sirsi.net/client/en_US/default/search/results?qu=")
    AddSetting(conn, 'SEARCH_URL_SUFFIX', '&te=&te=ILS')
    AddSetting(conn, 'PAGE_LINK_PREFIX', 'https://mobi.ent.sirsi.net')
    # AddSetting(conn, 'FILE_PATH', './')
    AddSetting(conn, 'TITLE_ELEMENT_MULTIPLE', '.results_bio')
    AddSetting(conn, 'TITLE_ELEMENT_SINGLE', 'div.text-p.INITIAL_TITLE_SRCH')
    AddSetting(conn, 'PUBDATE_ELEMENT_RESULTS', 'displayElementText text-p highlightMe PUBDATE')
    AddSetting(conn, 'PUBDATE_ELEMENT_PAGE', '.text-p.PUBLICATION_INFO')
    # AddSetting(conn, 'INPUT_DATA', 'movies.csv')

def AddSetting(conn, setting, value):
    # print("Initializing settings table...")
    query = """
            INSERT INTO settings 
                (setting_name,
                 setting_value) 
            VALUES (:setting, :value)    
            """
    return ExecuteQuery(conn, query, {"setting": setting, "value": value}) #(conn, query, query_parameters)
    


def main():
    db_file = "./movies.db"
    
    conn = ConnectToDatabase(db_file)

    # if there is no database file, create the database file and necessary databases
    if not conn:
        CreateDatabaseFile(db_file)
        conn = ConnectToDatabase(db_file)
        CreateMoviesDatabase(conn)
        CreateResultsDatabase(conn)
        CreateSettingsDatabase(conn)
    
    # ----- All databases should be setup ----- #

    # setup the initial settings: URLs, classes to find tags, etc
    InitializeSettings(conn)

    CloseDatabaseConnection(conn)


if __name__ == "__main__":
    main()
