from fastapi import APIRouter, Body, Request, Response, HTTPException, status, Path
from fastapi.encoders import jsonable_encoder
from typing import List
from urllib.parse import unquote
from models import Movie, MovieUpdate
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId

router = APIRouter()
PyObjectId = Annotated[str, BeforeValidator(str)]



@router.get("/", response_description="List all movies", response_model=List[Movie])
def list_movies(request: Request):
    movies = list(request.app.database["movies"].find(limit=100))
    return movies

@router.get("/{id}", response_description="Get a single movie by id", response_model=Movie)
def find_movie(id: str, request: Request):
    object_id = ObjectId(id)
    print(type(object_id))
    if (movies := request.app.database["movies"].find_one({"_id": object_id})) is not None:
        return movies
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movies with ID {id} not found")

@router.put("/{id}", response_description="Update a movie", response_model=Movie)
def update_movie(id: str, request: Request, movies: MovieUpdate = Body(...)):
    object_id = ObjectId(id)
    movies = {k: v for k, v in movies.dict().items() if v is not None}
    if len(movies) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"_id": object_id}, {"$set": movies}
        )

        # if update_result.modified_count == 0:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with ID {id} not found")

    if (
        existing_movies := request.app.database["movies"].find_one({"_id": object_id})
    ) is not None:
        return existing_movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with ID {id} not found")

@router.delete("/{id}", response_description="Delete a movie")
def delete_movie(id: str, request: Request, response: Response):
    delete_result = request.app.database["movies"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movies with ID {id} not found")


@router.get("/search/{actor_or_title}", response_description="Get movies by actor or title", response_model=List[Movie])
def find_movies_by_actor(actor_or_title: str, request: Request):
    decoded_actor_or_title = unquote(actor_or_title).replace("%20", " ")

    movies = list(request.app.database["movies"].find({"$or":[{"title": decoded_actor_or_title},{"cast": decoded_actor_or_title}]}))

    if movies:
        return movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No movies found for actor or title {decoded_actor_or_title}")

@router.put("/update/{movie_title}", response_description="Update a movie by title", response_model=Movie)
def update_movie(movie_title: str, request: Request, movies: MovieUpdate = Body(...)):
    movies = {k: v for k, v in movies.dict().items() if v is not None}
    if len(movies) >= 1:
        update_result = request.app.database["movies"].update_one(
            {"title": movie_title}, {"$set": movies}
        )

        # if update_result.modified_count == 0:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with title {id} not found")

    if (
        existing_movies := request.app.database["movies"].find_one({"title": movie_title})
    ) is not None:
        return existing_movies

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"movie with title {movie_title} not found")

