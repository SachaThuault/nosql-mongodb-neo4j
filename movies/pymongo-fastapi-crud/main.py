from fastapi import FastAPI
from pymongo import MongoClient
from routes import router as movie_router
from py2neo import Graph

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    # 2 lignes qui suivent servent à la connexion à la MongoDB, à adapter avec votre URI et nom de base de données
    app.mongodb_client = MongoClient("mongodb+srv://BDD_NoSQL_USER:KidoER35AZ@project.ls9qqzu.mongodb.net/?retryWrites=true&w=majority")
    app.databaseMongo = app.mongodb_client['Project']
    # Adapter la ligne qui suit avec vos paramètres de la bdd Neo4
    app.databaseNeo4j = Graph("bolt://3.95.167.94:7687", auth=("neo4j", "stators-guys-brooks"))
    if(app.databaseNeo4j):
        print('\n    Connexion avec Neo4j réussie : \n', app.databaseNeo4j)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(movie_router, tags=["movies"], prefix="/movies")