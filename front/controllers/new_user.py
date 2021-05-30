import pickle
import pandas as pd
import mysql.connector
from mysql.connector import errorcode
import math
import sys
import csv
import sys, getopt
import json
import os
import numpy as np
import pandas as pd
import seaborn as sns
from surprise import Reader
from surprise import Dataset
from surprise.model_selection import train_test_split
from surprise import KNNBasic
from surprise import accuracy
import random

def main(argv):
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
  #print ('First argument:',  str(argv))
  file_path = './controllers/Artistas_Final.csv'
  ratings=pd.read_csv(file_path, sep = '\t', header=0, names = ["user_id","artist_name","rating"] )
  ratings = ratings.loc[:,["user_id","artist_name","rating"]]

  reader = Reader( rating_scale = ( 0, 5.00 ) )
  
  user_id= str(argv)
  sql_artists = "SELECT user_id,artist_name,score as rating from preferences_artists where user_id ="+ user_id
  #cursor.execute(sql_artists)
  ratings =  ratings[ :20000]
  ratings = ratings[ ["user_id","artist_name","rating"] ]
  print(ratings.head())
  ratings = ratings.append(pd.read_sql(sql_artists, cnx))
  #print(df)
  
  #Se crea el dataset a partir del dataframe
  surprise_dataset = Dataset.load_from_df( ratings[ ["user_id","artist_name","rating"] ], reader )

  print("{\"message\":\" ")  
  train_set, test_set=  train_test_split(surprise_dataset, test_size=.2)
  sim_options = {'name': 'cosine',
               'user_based': True  # calcule similitud item-item
               }
  algo = KNNBasic(k=50, min_k=10, sim_options=sim_options)
  algo.fit(train_set)
  predictions=algo.test(test_set)
  pd_predictions=pd.DataFrame(predictions)
  user_predictions=list(filter(lambda x: x[0]==argv,predictions))
  #print("predictions",user_predictions)

  
  
  sql = "INSERT INTO `recomendations_artists` (`user_id`, `artist_name`,`recomendation_score`,`model`,`tipo_modelo`) VALUES (%s, %s, %s,'coseno','user')"
  print(" \" },")
  ##persistirlo en la tabla
  def isNaN(string):
      return string != string
  
  for i in pd_predictions.index: 
      cursor.execute(sql, (int(pd_predictions['uid'][i]),pd_predictions['iid'][i],float(pd_predictions['est'][i])))
      cnx.commit()
  del pd_predictions
  
  cursor.close()
  cnx.close()
  
  send_message_back = {
    'arguments': argv,
    'message': """Hello,
  This is my message.
  To the world"""
  }
  print(json.dumps(send_message_back))
  
if __name__ == "__main__":
    main(sys.argv[1])