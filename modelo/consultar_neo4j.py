from datetime import datetime
from typing import ValuesView
import pandas as pd
from neo4j import GraphDatabase
import py2neo

#Se abre la sesión de Neo4j
session = py2neo.Graph(host='localhost', user='neo4j', password='srneo4j-pass')

#Consultar Peliculas en Neo4j

query_peliculas = "MATCH (m:Peliculas) RETURN m.id AS id, m.id_imdb AS id_imdb, m.nombre AS nombre, m.duracion AS duracion, m.rating_imdb AS rating_imdb"
df_resultados_peliculas = session.run(query_peliculas).to_data_frame()
print(df_resultados_peliculas)

#Consultar Los retings dados por los usuarios a las peliculas en Neo4j

query_usuarios_rating_peliculas = "MATCH (u:Usuarios)-[r:califica]->(m:Peliculas) RETURN u.id AS usuario_id, r.rating AS rating, m.id AS pelicula_id, m.id_imdb AS pelicula_id_imdb, m.nombre AS pelicula_nombre, m.duracion AS pelicula_duracion, m.rating_imdb AS pelicula_rating_imdb"
df_resultados_usuarios_rating_peliculas = session.run(query_usuarios_rating_peliculas).to_data_frame()
print(df_resultados_usuarios_rating_peliculas)
