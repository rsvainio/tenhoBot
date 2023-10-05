import sqlite3
import sys
import random

dbConn = None
database = 'database.db'

def connectDatabase(database: str):
    conn = sqlite3.connect(f'databases/{database}')
    print('connected to database:', database)
    global dbConn
    dbConn = conn

#TODO make this more abstract, (i.e. accept a list of values and parse the sql syntax to understand what the command is)
def incrementUser(value1: str):
    if dbConn == None:
        connectDatabase(database)
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

def addEntry(values: tuple, table: str):
    if dbConn == None:
        connectDatabase(database)
    cursor = dbConn.cursor()
    sql = f'INSERT INTO {table} VALUES {values}'
    
    try:
        cursor.execute(sql)
        dbConn.commit()
    #TODO add logging here
    except sqlite3.ProgrammingError() as e:
        print(e)

def fetchResponse():
    if dbConn == None:
        connectDatabase(database)
    cursor = dbConn.cursor()

    sql = 'SELECT * FROM Responses ORDER BY RANDOM() LIMIT 1'
    cursor.execute(sql)
    return cursor.fetchone()

def databaseReset():
    if dbConn == None:
        connectDatabase(database)

    cursor = dbConn.cursor()
    cursor.execute("SELECT name FROM sqlite_schema WHERE type='table';")
    dropTables = cursor.fetchall()
    for t in dropTables:
        cursor.execute(f'DROP TABLE {t[0]};')

    #add more tables as needed
    tables = []
    tables.append(""" CREATE TABLE Repostimies (
                Username VARCHAR(32) NOT NULL,
                Num_reacted INT
            );""")
    tables.append(""" CREATE TABLE Responses (
                Author VARCHAR(32) NOT NULL,
                Response VARCHAR(255) NOT NULL
            );""")
    for t in tables:
        cursor.execute(t)

    dbConn.close()
    print(f'{database} reset succesfully')

if __name__ == '__main__':
    globals()[sys.argv[1]]()