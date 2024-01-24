from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as movie_router

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["LOCALHOST_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(movie_router, tags=["movies"], prefix="/movies")


# from fastapi import FastAPI
# from pymongo import MongoClient
# from routes import router as movie_router
#
# app = FastAPI()
#
# @app.on_event("startup")
# def startup_db_client():
#     app.mongodb_client = MongoClient("mongodb+srv://tatdevelops:gjKSGbujMNz7llJs@bddnosql.soetk4a.mongodb.net/?retryWrites=true&w=majority")
#     app.databaseMongo = app.mongodb_client['bddnosql']
#
# @app.on_event("shutdown")
# def shutdown_db_client():
#     app.mongodb_client.close()
#
# app.include_router(movie_router, tags=["movies"], prefix="/movies")