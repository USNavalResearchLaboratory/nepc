import mysql.connector

def connect():
    config = {
        'user': 'nepc',
        'password': 'nepc',
        'host': 'localhost',
        #'host': '132.250.158.124',
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

def model(cursor, modelName):
    cursor.execute("SELECT cs.cs_id as cs_id " +
               "FROM cs " +
               "JOIN models2cs m2cs ON (cs.cs_id = m2cs.cs_id) " +
               "JOIN models m ON (m2cs.model_id = m.model_id) " +
               "WHERE m.name LIKE '" + modelName + "'" )
    csArray = cursor.fetchall()
    for csItem in csArray:
        cs_id = csItem[0]
        #print(cs_id)
        cursor.execute("SELECT * FROM cs WHERE cs_id = " + str(cs_id))
        csMetadata = cursor.fetchall()[0]
        print(csMetadata)
        cursor.execute("SELECT e, sigma FROM csdata WHERE cs_id = " + str(cs_id))
        csData = cursor.fetchall()
        print(csData)
