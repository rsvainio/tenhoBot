import sqlite3
from threading import Lock

mutex = Lock()
dbConn = None
database = 'repostimies.db'

def dbConnectDatabase(database):
    conn = sqlite3.dbConnect(f'databases/{database}')
    print('dbConnected to database:', database)
    dbConn = conn

def updateDatabase(value1):
    if dbConn == None:
        dbConnectDatabase(database)
    with mutex:
        print('Starting query')
        cursor = dbConn.cursor()

        #TODO fix this shit
        sql = f'UPDATE Repostimies SET Num_reacted = 2 WHERE Username = ?'
        cursor.execute(sql, [(value1)])

        dbConn.commit()

def databaseReset(database):
    if dbConn == None:
        dbConnectDatabase(database)

    cursor = dbConn.cursor()
    cursor.execute('DROP TABLE IF EXISTS Repostimies')

    table = """ CREATE TABLE Repostimies (
                Username VARCHAR(25) NOT NULL,
                Num_reacted INT
            );"""

    cursor.execute(table)

    dbConn.close()
    print(f'Database: {database} reset succesfully')