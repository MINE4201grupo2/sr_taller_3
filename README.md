# sr_taller_3
Taller 2 sistemas de recomendación

## preprocesamiento
Esta carpeta contiene los archicos para carga de información
active_user.csv
- Analisis_descriptivo.ipynb: contiene el análisis descripttivo de las diferentes bases
- load_active_users.py: carga los usuarios activos a base de datos para su inicio de sesión, un usuario activo es aquel que en la base de reseñas haya hecho al menos 5 reseñas.
- load_movies.py: carga toda la base de peliculas a base de datos

## modelo
Esta carpeta contiene los modelo y las bases preprocesadas para que este corra.

- FiltradoColaborativo.ipynb: contiene el modelo con el cual se calcularon las recomendaciones, e inserta a base de datos.
- Modelo.ipynb contiene el modelo hibrido de filtrado ontologico (contenido) y filtrado colaborativo usuario usuario
- insertar_neo4j.py contiene la información para insertar los datos a neo4j y extraer la información de la librería imdb
- consultar_neo4j.py contiene las queries para realizar las consultas a la BD de neo4j con el fin de correr el modelo posteriormente

## sql
Contiene la información de la creación de la base de datos y las tablas requeridas para el funcionamiento del modelo.
- contiene los procedimientos almacenados para las queries que realiza el front


## run node
- La pagina web no maneja excepciones por lo tanto si se presenta una excepción de sql el servicio se cae y toca volverlo a subir. Para subir el servicio se ingresa al servidor y se corre el siguiente comando forever start bin/www.
- Correr en desarrollo: npm run dev
