import mysql.connector
import connect



dbconn = None
connection = None
def getCursor(): 
  try:
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn
  except Exception as e:
    print("Error happen in Database connection : %s",e)