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

#Lectura del dataframe
columns_data = ['userId','timestamp','musicbrainz-artist-id', 'artist-name','trackId','trackname']

#df_use_habits= pd.DataFrame(columns = ['userId','timestamp','musicbrainz-artist-id', 'artist-name','trackId','trackname'])
df_artist= pd.DataFrame(columns = ['musicbrainz-artist-id', 'artist-name'])
df_tracks= pd.DataFrame(columns = ['trackId','trackname'] )

chunksize = 10 ** 6
#with pd.read_csv('data/userid-timestamp-artid-artname-traid-traname.tsv', encoding="utf-8", delimiter='\r', chunksize=chunksize, header=None) as reader:
with pd.read_csv('data/clean.tsv', encoding="utf-8", delimiter='\t', chunksize=chunksize, header=None, names=columns_data) as reader:
    for chunk in reader:
        df_artist = df_artist.append(chunk[['musicbrainz-artist-id', 'artist-name']])
        df_tracks = df_tracks.append(chunk[['trackId','trackname']])
#print(df_artist)
print("Finish reading file and dtaframes")
# Remove duplicates
df_artist= df_artist.drop_duplicates(keep='first')
df_artist = df_artist.reset_index(drop=True)
df_tracks= df_tracks.drop_duplicates(keep='first')
df_tracks = df_tracks.reset_index(drop=True)


# Create a new record
sql_tracks = "INSERT INTO `tracks` (`music_track_id`, `music_track_name`) VALUES (%s, %s)"
sql_artists = "INSERT INTO `artists` (`music_artist_id`, `music_artist_name`) VALUES (%s, %s)"

def isNaN(string):
    return string != string

for i in df_tracks.index: 
  # Execute the query
  var1= None if isNaN(df_tracks['trackId'][i]) else ''.join([c for c in df_tracks['trackId'][i].strip() if c not in ['\t', '\n', '\f', '\r','\u000B','\u0085','\u2028','\u2029','\u0022', '\u005C', '\u0027', '"']]) 
  var2= None if isNaN(df_tracks['trackname'][i]) else ''.join([c for c in df_tracks['trackname'][i].strip() if c not in ['\t', '\n', '\f', '\r','\u000B','\u0085','\u2028','\u2029','\u0022', '\u005C', '\u0027', '"']]) 
  #print(var2)
  
  try:
    cursor.execute(sql_tracks, (var1,var2))
  except mysql.connector.errors.DataError as err:
    print("Track var 1: "+ var1+ " ")
    print("Track var 2: "+ var2+ " ")
    print("nooooo" + df_tracks['trackname'][i])
    sys.exit(1)
  
  # the connection is not autocommited by default. So we must commit to save our changes.
  cnx.commit()

for i in df_artist.index: 
  # Execute the query
  var1= None if isNaN(df_artist['musicbrainz-artist-id'][i]) else ''.join([c for c in df_artist['musicbrainz-artist-id'][i].strip() if c not in ['\t', '\n', '\f', '\r','\u000B','\u0085','\u2028','\u2029','\u0022', '\u005C', '\u0027', '"']])
  var2= None if isNaN(df_artist['artist-name'][i]) else ''.join([c for c in df_artist['artist-name'][i].strip() if c not in ['\t', '\n', '\f', '\r','\u000B','\u0085','\u2028','\u2029','\u0022', '\u005C','\u0027', '"' ]]) 
  #print(var2)
  try:
    cursor.execute(sql_artists, (var1,var2))
  except mysql.connector.errors.DataError as err:
    print("Artists var 1: "+ var1+ " ")
    print("Artists var 2: "+ var2+ " ")
    sys.exit(1)
  # the connection is not autocommited by default. So we must commit to save our changes.
  cnx.commit()

#print(df_artist)
cursor.close()
cnx.close()