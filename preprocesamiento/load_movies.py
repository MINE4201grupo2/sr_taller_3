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
columns_data = ['movieId','title','genres']

df= pd.DataFrame(columns = ['movieId','title','genres'])

CURR_DIR = os.getcwd()
print(CURR_DIR)

chunksize = 10 ** 6

business_json_path = CURR_DIR+'/ml-25m/movies.csv'
df_b= pd.read_csv(business_json_path)

#df_explode = df_b.assign(categories = df_b.categories
#                         .str.split(', ')).explode('categories')
#df_explode=df_explode.reset_index()
#df_explode

print("Finish reading file and dtaframes")

# Create a new record
sql = "INSERT INTO `movies` (`movies_id`, `title`, `genres`) VALUES (%s, %s, %s)"


def isNaN(string):
    return string != string
print(df_b.index)
for i in df_b.index: 
  # Execute the query
  var1= df_b['movieId'][i]
  var2= df_b['title'][i]
  var3= df_b['genres'][i]


  try:
    #print(var1,var2,var3)
    cursor.execute(sql, (int(var1),var2,var3))
  except mysql.connector.errors.DataError as err:
    print("Track var 1: "+ var1+ " ")
    sys.exit(1)
  
  # the connection is not autocommited by default. So we must commit to save our changes.
  cnx.commit()


#print(df_artist)
cursor.close()
cnx.close()