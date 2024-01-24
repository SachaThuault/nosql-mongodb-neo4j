from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Path
from typing import List
from urllib.parse import unquote

from fastapi.responses import JSONResponse
from models import Movie, MovieUpdate, MoviesNeo4J
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

router = APIRouter()
PyObjectId = Annotated[str, BeforeValidator(str)]

# list all movies (mongoDB)
@router.get("/mongodb", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    print(request.app.databaseMongo)
    movies = list(request.app.databaseMongo["movies"].find(limit=100))
    return movies

@router.get("/mongodb/{id}", response_description="Get a single movie by id", response_model=Movie)
def find_movie(id: str, request: Request):
    object_id = ObjectId(id)
    print(type(object_id))
    if (movies := request.app.databaseMongo["movies"].find_one({"_id": object_id})) is not None:
        return movies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movies with ID {id} not found")

@router.put("/mongodb/{id}", response_description="Update a movie", response_model=Movie)
def update_movie(id: str, request: Request, movies: MovieUpdate = Body(...)):
    object_id = ObjectId(id)
    movies = {k: v for k, v in movies.dict().items() if v is not None}
    if len(movies) >= 1:
        update_result = request.app.databaseMongo["movies"].update_one(
            {"_id": object_id}, {"$set": movies}
        )

    if (
        existing_movies := request.app.databaseMongo["movies"].find_one({"_id": object_id})
    ) is not None:
        return existing_movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with ID {id} not found")

@router.delete("/mongodb/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.databaseMongo["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movies with ID {id} not found")

#  list a specific movie - the name of the movie or the name of the actor are given in parameter
@router.get("/mongodb/search/{actor_or_title}", response_description="Get movies by actor or title", response_model=List[Movie])
def find_movies_by_actor(actor_or_title: str, request: Request):
    decoded_actor_or_title = unquote(actor_or_title).replace("%20", " ")

    movies = list(request.app.databaseMongo["movies"].find({"$or":[{"title": decoded_actor_or_title},{"cast": decoded_actor_or_title}]}))

    if movies:
        return movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No movies found for actor or title {decoded_actor_or_title}")

#  update informa3on about a specific movie - the name of the movie is given in parameter
@router.put("/mongodb/update/{movie_title}", response_description="Update a movie by title", response_model=Movie)
def update_movie(movie_title: str, request: Request, movies: MovieUpdate = Body(...)):
    movies = {k: v for k, v in movies.dict().items() if v is not None}
    if len(movies) >= 1:
        update_result = request.app.databaseMongo["movies"].update_one(
            {"title": movie_title}, {"$set": movies}
        )

    if (
        existing_movies := request.app.databaseMongo["movies"].find_one({"title": movie_title})
    ) is not None:
        return existing_movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with title {movie_title} not found")

@router.get("/neo4j", response_description="List all movies from Neo4J", response_model=List[MoviesNeo4J])
def list_movies_neo4j(request: Request):
    graph = request.app.databaseNeo4j
    result = graph.run("MATCH (m:Movie) RETURN m")
    print(result)
    movies_data = [record["m"] for record in result]
    movies_mapped = [map_movie_to_model(movie) for movie in movies_data]

    return movies_mapped

# return the number of movies common between mongoDB database & neo4j database
@router.get("/common-movies", response_description="Number of common movies between MongoDB and Neo4J", response_model=int)
def count_common_movies(request: Request):
    graph = request.app.databaseNeo4j
    neo4j_result = graph.run("MATCH (m:Movie) RETURN m")
    neo4j_movies = set(record["m"]["title"] for record in neo4j_result)

    mongo_db = request.app.databaseMongo
    mongo_result = list(mongo_db["movies"].find(limit=100))
    mongo_movies = set(movie["title"] for movie in mongo_result)

    common_movies = neo4j_movies.intersection(mongo_movies)
    num_common_movies = len(common_movies)

    return num_common_movies

# list users who rated a movie - the name of the movie is given in parameter ex : "The Da Vinci Code"
@router.get('/neo4j/{title}')
def get_movie_by_title(request: Request, title: str = Path(..., title="Title")):
    decoded_title = unquote(title).replace("%20", " ")
    cypher_query = (
        "MATCH (p1)-[r]->(m) WHERE (p1:Person) AND (m:Movie) AND m.title = $title AND r:REVIEWED RETURN m.title AS `Title`, collect({ Reviewers: p1.name, Ratings: r.rating}) AS `Reviewers`"
    )
    result = request.app.databaseNeo4j.run(cypher_query, title=decoded_title).data()
    return result

# return a user with the number of movies he has rated and the list of rated movies - the name of the user is given in parameter
# ex : "James Thompson"
@router.get('/neo4j/user/{user}')
def get_rated_movies_by_user(request: Request, user: str = Path(..., title="User")):
    decoded_user = unquote(user).replace("%20", " ")
    cypher_query = (
        "MATCH (p)-[r]->(m) WHERE p.name = $decoded_user AND (p:Person) AND (m:Movie) AND (r:REVIEWED) RETURN p.name AS `Name`, count(m) AS `Number of rated movies`, collect(m.title) AS `Movie(s)`"
    )
    result = request.app.databaseNeo4j.run(cypher_query, decoded_user=decoded_user).data()

    if result:
        result = result[0]

    return JSONResponse(content=result)

def map_movie_to_model(movie):
    movie_model = MoviesNeo4J(**{
        "id": movie.get("id"),
        "released": movie["released"],
        "tagline": str(movie.get("tagline", "")),  
        "title": movie["title"],
    })
    
    return movie_model



