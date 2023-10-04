import sqlite3
from threading import Lock

mutex = Lock()
dbConn = None
database = 'repostimies.db'

def connectDatabase(database):
    conn = sqlite3.connect(f'databases/{database}')
    print('connected to database:', database)
    global dbConn
    dbConn = conn

#TODO make this more abstract, (i.e. accept a list of values and parse the sql syntax to understand what the command is)
def queryDatabase(value1):
    if dbConn == None:
        connectDatabase(database)
    with mutex:
        cursor = dbConn.cursor()

        #TODO should make this more dynamic
        sql = 'SELECT Username FROM Repostimies WHERE Username = ?'
        cursor.execute(sql, [(value1)])

        if cursor.fetchone():
            print(f'Incrementing the Num_reacted value of user: {value1}')
            sql = 'UPDATE Repostimies SET Num_reacted = Num_reacted + 1 WHERE Username = ?'
        else:
            print(f'User {value1} not found within the database, inserting...')
            sql = 'INSERT INTO Repostimies VALUES (?, 1)'

        try:
            cursor.execute(sql, [(value1)])
            dbConn.commit()
        #TODO add logging here
        except sqlite3.ProgrammingError() as e:
            print(e)

def databaseReset(database):
    if dbConn == None:
        connectDatabase(database)

    cursor = dbConn.cursor()
    cursor.execute('DROP TABLE IF EXISTS Repostimies')

    table = """ CREATE TABLE Repostimies (
                Username VARCHAR(25) NOT NULL,
                Num_reacted INT
            );"""

    cursor.execute(table)

    dbConn.close()
    print(f'Database: {database} reset succesfully')