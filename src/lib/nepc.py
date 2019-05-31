import mysql.connector

def connect():
    config = {
        'user': 'nepc',
        'password': 'nepc',
        'host': '132.250.158.124',
        'database': 'nepc',
        'raise_on_warnings': True
    }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    return cnx, cursor

def printTable(cursor, table):
    print("\n=========================\n " + table + ":\n=========================")
    cursor.execute("select * from " + table + ";")
    for x in cursor:
        print(x) 

def countTableRows(cursor, table):
    print("\nRows in " + table + ": ") 
    cursor.execute("select count(*) from " + table + ";")
    for x in cursor:
        print(x) 

