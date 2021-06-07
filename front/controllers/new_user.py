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
import pandas as pd
from rake_nltk import Rake
#pip install rake-nltk
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

def main(argv):
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
  # Print arguments one by one
  print ('First argument:',  str(argv))
  file_path = './movies_bagofwords.csv'
  df=pd.read_csv(file_path, sep = ',', header=0, names = ["movieId","title","bagofwords"] )
  # instantiating and generating the count matrix
  count = CountVectorizer()
  count_matrix = count.fit_transform(df['bagofwords'])

  # generating the cosine similarity matrix
  cosine_sim = cosine_similarity(count_matrix, count_matrix)
  cosine_sim 

  # list I will use in the function to match the indexes
  indices = pd.Series(df.index)

  #  defining the function that takes in movie title 
  # as input and returns the top 10 recommended movies
  def recommendations(title, cosine_sim = cosine_sim):

      # initializing the empty list of recommended movies
      recommended_movies = []
      try:
          # gettin the index of the movie that matches the title
          idx = indices[indices == title].index[0]

          # creating a Series with the similarity scores in descending order
          score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)

          # getting the indexes of the 10 most similar movies
          top_10_indexes = list(score_series.iloc[1:11].index)

          # populating the list with the titles of the best 10 matching movies
          for i in top_10_indexes:
              recommended_movies.append(list(df.index)[i])
      except:
          i=0
          #print("not recomend")
      return recommended_movies

  user_id= str(argv)
  #user_id = 162543
  sql_artists = "SELECT user_id,movie_id,score as rating from preferences where user_id ="+ user_id
  #cursor.execute(sql_artists)
  ratings = pd.DataFrame()
  ratings = ratings.append(pd.read_sql(sql_artists, cnx))
  print(df)

  # load the model from disk
  import pickle
  filename = 'filtrado_colaborativo.sav'
  loaded_model = pickle.load(open(filename, 'rb'))

  movies= pd.read_csv('ml-latest-small/movies.csv')
  unique_movies = movies.movieId.unique().shape[0]
  unique_users = 1
  matrix_all = np.zeros((unique_users, unique_movies))
  movies['movie_id_simple'] = pd.factorize(movies.moviesId)[0]

  sql = "INSERT INTO `recomendations_movies` (`user_id`, `movie_id`, `recomendation_score`) VALUES (%s, %s, %s)"

  for i in range(0,unique_users):
      #print(user_id)
      for k in ratings.index:
          business_id = movies['movieId'][k]
          #print(business_id)
          list_rec = recommendations(business_id)
          if len(list_rec) >0:
              for k in list_rec:
                  cursor.execute(sql, (str(user_id),str(k),5))
                  cnx.commit()
          
  
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