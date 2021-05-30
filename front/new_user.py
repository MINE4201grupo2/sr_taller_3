import pickle
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import math
import sys
import csv

#Configuración de la conexión a Mysql
try:
  cnx = mysql.connector.connect(user='user_taller1', password='taller1.', host='127.0.0.1', database='taller1')
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

cursor = cnx.cursor()
# Print arguments one by one
print ('First argument:',  str(sys.argv[0]))

user_id= str(sys.argv[1])

sql_artists = "SELECT user_id,artist_name,score as rating from preferences_artists where user_id ="+ user_id
cursor.execute(sql_artists)

#df= pd.read_sql(sql, cnx)
#print(df)

filename = 'artist_coseno_user_model.sav'
loaded_model = pickle.load(open(filename, 'rb'))
# Preguntar BD por el usuario
#obtener pferencias
## correr el modelo
predictions = loaded_model.test(cursor.fetchall())
pd_predictions=pd.DataFrame(predictions)
pd_predictions
sql = "INSERT INTO `recomendations_artists` (`user_id`, `artist_name`,`recomendation_score`,`model`,`tipo_modelo`) VALUES (%s, %s, %s,'coseno','user')"
##persistirlo en la tabla
def isNaN(string):
    return string != string

for i in pd_predictions.index: 
    cursor.execute(sql, (int(pd_predictions['uid'][i]),pd_predictions['iid'][i],float(pd_predictions['est'][i])))
    cnx.commit()
del pd_predictions

cursor.close()
cnx.close()