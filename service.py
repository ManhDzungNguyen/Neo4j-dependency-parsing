import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from function import import_articles
from entity import ListArticle


app = FastAPI(title="Import Documents to Neo4j DB")
MAX_IMPORT_ARTICLES = 20

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/import_data")
async def import_data(item: ListArticle):
    data = item.docs
    data = data[:MAX_IMPORT_ARTICLES]

    output = import_articles(data)
    return output
