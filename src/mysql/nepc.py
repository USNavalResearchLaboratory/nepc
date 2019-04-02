import mysql.connector

mydb = mysql.connector.connect(
	host='localhost',
	option_files='/home/adamson/.mysql/defaults'
)

mycursor = mydb.cursor()

mycursor.execute("DROP DATABASE IF EXISTS `nepc`;")
mycursor.execute("CREATE DATABASE IF NOT EXISTS `nepc`;")
mycursor.execute("SET default_storage_engine = INNODB;")

mycursor.execute("SHOW DATABASES")

for x in mycursor:
  print(x) 
