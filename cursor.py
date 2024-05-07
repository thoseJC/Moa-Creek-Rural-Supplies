import mysql.connector
import connect
import sys


dbconn = None
connection = None
def getCursor(): 
  global dbconn
  global connection
  connection = mysql.connector.connect(user=connect.dbuser, \
  password=connect.dbpass, host=connect.dbhost, \
  database=connect.dbname, autocommit=True)
  dbconn = connection.cursor()
  return dbconn

# sys.modules[__name__] = getCursor