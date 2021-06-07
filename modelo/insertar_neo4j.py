from datetime import datetime
from typing import ValuesView
import pandas as pd
from neo4j import GraphDatabase
import imdb
   
#Inicializar instancia de IMDb
ia = imdb.IMDb()

uri = "neo4j://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "srneo4j-pass"))

#Se abre la sesión de Neo4j
session = driver.session()

#Se elimina todo el contenido de la base de datos
session.run("MATCH (n) DETACH DELETE n")

#Lectura de los datasets
df_ratings=pd.read_csv('datos/ratings.csv')
df_movies= pd.read_csv('datos/movies.csv')
df_links= pd.read_csv('datos/links.csv')
df_users= pd.read_csv('datos/users.csv')

#Preparación del dataset: movies
#print(df_movies)

#Preparación del dataset: ratings
df_ratings['timestamp'] = df_ratings['timestamp'].apply(datetime.fromtimestamp)
#print(df_ratings)

#Preparación del dataset: users
#print(df_users)

#Union de los dataset por nodos
df_movies_link = df_movies.merge(df_links, on = 'movieId', how = 'inner')
#print(df_movies_link)

#'Wallace & Gromit: The Best of Aardman Animation (1996)'
#dc_movie_data = ia.get_movie('0118114')
#print(dc_movie_data)

#Insertar nodo usuarios en Neo4j

for i in df_users.index:

    print('usuario: '+str(df_users["userId"][i]))
    session.run("CREATE (u:Usuarios {id:'"+str(df_users["userId"][i])+"'})")

#Insertar nodos peliculas, generos, personas y relaciones actor_en, director_en, tiene_genero en Neo4j

for i in df_movies_link.index:
    
    rating_imbd = 0.0
    runtimes = 0.0
    
    print('pelicula: '+str(df_movies_link["title"][i]).replace("'",""))
    
    try:
        dc_movie_data = ia.get_movie(str(df_movies_link["imdbId"][i]))

        rating_imbd = dc_movie_data['rating']
        runtimes = dc_movie_data['runtimes'][0]
        
        #for key, value in dc_movie_data.items():
        #    print(str(key)+': '+str(value)) 
        
        #Insertar nodo de generos

        for genero in dc_movie_data['genres']:
            
            session.run("MERGE (g:Generos {nombre:'"+str(genero)+"'})"
                        +" ON CREATE "
                        +"SET g.nombre = '"+str(genero)+"'")

        #Insertar nodo de personas

        for actor in dc_movie_data['actors']:
            
            session.run("MERGE (p:Personas {id:'"+str(actor.personID)+"'})"
                        +" ON CREATE "
                        +"SET p.nombre = '"+str(actor['name']).replace("'","")+"'")

        for director in dc_movie_data['directors']:
            
            session.run("MERGE (p:Personas {id:'"+str(director.personID)+"'})"
                        +" ON CREATE "
                        +"SET p.nombre = '"+str(director['name']).replace("'","")+"'")

        #Insertar nodo de peliculas

        session.run("CREATE (a:Peliculas {id:'"+str(df_movies_link["movieId"][i])
                    +"',id_imdb:'"+str(df_movies_link["imdbId"][i])
                    +"',nombre:'"+str(df_movies_link["title"][i]).replace("'","")
                    +"',duracion:'"+str(runtimes)
                    +"',rating_imdb:'"+str(rating_imbd)+"'})")
        
        #Insertar relación director_en

        for director in dc_movie_data['directors']:

            session.run("MATCH (p:Peliculas), (d:Personas) WHERE p.id = '"+str(df_movies_link["movieId"][i])+"' AND d.id = '"+str(director.personID)+"'"
                        +"CREATE (d)-[r:director_en]->(p)")

        #Insertar relación actor_en

        for actor in dc_movie_data['actors']:

            session.run("MATCH (p:Peliculas), (d:Personas) WHERE p.id = '"+str(df_movies_link["movieId"][i])+"' AND d.id = '"+str(actor.personID)+"'"
                        +"CREATE (d)-[r:actor_en]->(p)")
        
        #Insertar relación tiene_genero

        for genero in dc_movie_data['genres']:

            session.run("MATCH (p:Peliculas), (g:Generos) WHERE p.id = '"+str(df_movies_link["movieId"][i])+"' AND g.nombre = '"+str(genero)+"'"
                        +"CREATE (p)-[r:tiene_genero]->(g)")
    except:
        print('Pelicula no insertada')


#Insertar relación califica

for i in df_ratings.index:

    session.run("MATCH (p:Peliculas), (u:Usuarios) WHERE p.id = '"+str(df_ratings["movieId"][i])+"' AND u.id = '"+str(df_ratings["userId"][i])+"'"
                    +"CREATE (u)-[r:califica {rating: "+str(df_ratings["rating"][i])+"}]->(p)")
