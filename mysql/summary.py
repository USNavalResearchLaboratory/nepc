"""Prints a summary of the NEPC database"""
import mysql.connector
from nepc import nepc
from nepc.util import config

HOME = config.user_home()

########################
# Connect to database
########################
MYDB = mysql.connector.connect(
    host='localhost',
    option_files=HOME + '/.mysql/defaults'
)

MYCURSOR = MYDB.cursor()

MYCURSOR.execute("use nepc;")

########################
# Print a summary
########################
for table in ["species", "processes", "states", "cs", "models", "models2cs", "csdata"]:
    print(table + " has " + str(nepc.count_table_rows(MYCURSOR, table)) + " rows")
    print("===============================================\n")

MYCURSOR.close()

MYDB.close()
