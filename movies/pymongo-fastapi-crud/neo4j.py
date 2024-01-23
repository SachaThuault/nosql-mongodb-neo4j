from urllib.parse import unquote
from flask import Flask, jsonify, request
from py2neo import Graph

app = Flask(__name__)

# Remplace les informations ci-dessous par tes propres informations Neo4j
neo4j_uri = "bolt://3.219.31.15:7687"
username = "neo4j"
password = "thimbles-paragraphs-session"

# Initialiser la connexion à la base de données Neo4j
graph = Graph(neo4j_uri, auth=(username, password))

# Exemple de requête Neo4j
def run_neo4j_query(cypher_query):
    result = graph.run(cypher_query).data()
    return result

# Exemple de route pour exposer une requête Neo4j via l'API
@app.route('/api/exemple', methods=['GET'])
def exemple_api():
    cypher_query = "MATCH (n) RETURN n LIMIT 5"
    result = run_neo4j_query(cypher_query)
    return jsonify(result)


# list users who rated a movie - the name of the movie is given in parameter
@app.route('/api/<title>', methods=['GET'])
def get_movie_by_title(title):

    decoded_title = unquote(title).replace("%20", " ")
    print(decoded_title) # pour check le titre après traitement
    cypher_query = (
        "MATCH (p1)-[r]->(m) WHERE (p1:Person) AND (m:Movie) AND m.title = $decoded_title AND r:REVIEWED RETURN m.title AS `Title`, collect(p1.name) AS `Reviewers`, r.rating AS `Ratings`"
    )
    result = graph.run(cypher_query, decoded_title=decoded_title).data()
    return jsonify(result)

# return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter
@app.route('/api/user/<user>', methods=['GET'])
def get_rated_movies_by_user(user):

    decoded_user = unquote(user).replace("%20", " ")
    print(decoded_user)# pour check le nom du user après traitement
    cypher_query = (
        "MATCH (p)-[r]->(m) WHERE p.name = $decoded_user AND (p:Person) AND (m:Movie) AND (r:REVIEWED) RETURN p.name AS `Name`, count(m) AS `Number of rated movies`, collect(m.title) AS `Movie(s)`"
    )
    result = graph.run(cypher_query, decoded_user=decoded_user).data()
    return jsonify(result)



if __name__ == '__main__':
    app.run(debug=True)
