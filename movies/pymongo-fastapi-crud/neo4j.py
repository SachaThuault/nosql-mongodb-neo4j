from fastapi import FastAPI, Path
from urllib.parse import unquote
from py2neo import Graph

app = FastAPI()

# Remplace les informations ci-dessous par tes propres informations Neo4j
neo4j_uri = "bolt://3.95.167.94:7687"
username = "neo4j"
password = "stators-guys-brooks"

# Initialiser la connexion à la base de données Neo4j
graph = Graph(neo4j_uri, auth=(username, password))

# Fonction pour exécuter une requête Neo4j
def run_neo4j_query(cypher_query, **params):
    result = graph.run(cypher_query, **params).data()
    return result

# Exemple de route pour exposer une requête Neo4j via l'API
@app.get('/api/exemple')
def exemple_api():
    cypher_query = "MATCH (n) RETURN n LIMIT 5"
    result = run_neo4j_query(cypher_query)
    return result

# list users who rated a movie - the name of the movie is given in parameter ex : "The Da Vinci Code"
@app.get('/api/{title}')
def get_movie_by_title(title: str = Path(..., title="Title")):
    decoded_title = unquote(title).replace("%20", " ")
    cypher_query = (
        "MATCH (p1)-[r]->(m) WHERE (p1:Person) AND (m:Movie) AND m.title = $decoded_title AND r:REVIEWED RETURN m.title AS `Title`, collect({ Reviewers: p1.name, Ratings: r.rating}) AS `Reviewers`"

    )
    result = run_neo4j_query(cypher_query, decoded_title=decoded_title)
    return result

# return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter
# ex : "James Thompson"
@app.get('/api/user/{user}')
def get_rated_movies_by_user(user: str = Path(..., title="User")):
    decoded_user = unquote(user).replace("%20", " ")
    cypher_query = (
        "MATCH (p)-[r]->(m) WHERE p.name = $decoded_user AND (p:Person) AND (m:Movie) AND (r:REVIEWED) RETURN p.name AS `Name`, count(m) AS `Number of rated movies`, collect(m.title) AS `Movie(s)`"
    )
    result = run_neo4j_query(cypher_query, decoded_user=decoded_user)
    return result

# example : list_title = ["The Replacements", "The Da Vinci Code"]
@app.get('/api/movies_by_titles/{list_title}')
def get_movies_by_titles(list_title: str = Path(..., title="list_title")):
    decoded_list_title = unquote(list_title).replace('"', "")
    decoded1_list_title = unquote(decoded_list_title).replace("%20", " ")
    decoded2_list_title = unquote(decoded1_list_title).replace("]", "")
    final_decoded_list_title = unquote(decoded2_list_title).replace("[", "")
    titles_list = [title.strip() for title in final_decoded_list_title.split(",")]

    cypher_query = (
        "MATCH (m:Movie) WHERE m.title IN $titles_list RETURN DISTINCT m.title AS `Title`"
    )

    result = run_neo4j_query(cypher_query, titles_list=titles_list)
    return result

# MATCH (m)<-[]-() WHERE(m:Movie) AND m.title IN ["The Replacements", "The Da Vinci Code"] RETURN DISTINCT m.title AS `Title`