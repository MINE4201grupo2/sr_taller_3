import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import math
import sys
import csv
import os
import pandas as pd

#Configuración de la conexión a Mysql
try:
  cnx = mysql.connector.connect(user='user_taller3', password='taller3.', host='127.0.0.1', database='taller3')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()

#Lectura del dataframe
columns_data = ['userId']

df_users= pd.DataFrame(columns = ['userId'])

CURR_DIR = os.getcwd()
print(CURR_DIR)

chunksize = 10 ** 6

df_users= pd.read_csv('active_user.csv')
print("Finish reading file and dtaframes")

# Create a new record
sql_users = "INSERT INTO `users` (`user_id`,`email`, `password`) VALUES (%s, %s, %s)"

def isNaN(string):
    return string != string
var2 = 'fe3ce91a4a305670820fa708624a0f9f6c8c46770da510a5572c105dd0310333dfddfaaa29f76b76a4827bd0793896c5acad8d3240b1aaf7611ab224ff7a97d72c5e244e85af55af093f687af311dbcfcadccd460fe8610a6b1fee2386f323634d13604a'
for i in df_users.index: 
  # Execute the query
  var1=df_users['userId'][i]

  try:
    cursor.execute(sql_users, (int(var1),str(var1)+'@email.com',var2))
  except mysql.connector.errors.DataError as err:
    print("Track var 1: "+ var1+ " ")
    sys.exit(1)
  
  # the connection is not autocommited by default. So we must commit to save our changes.
  cnx.commit()


#print(df_artist)
cursor.close()
cnx.close()