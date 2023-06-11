import sys
sys.path.append("..")

import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

import db_session.db_engine as db_engine
from routers import actors, movies, subscriptions, token, users, movies_and_actors
from app.tmdb_data_retrieval.import_movies_in_db import fill_db_with_data_if_empty
from app.db_session.db_query_prepare import remove_duplicate_links
from app.db_session.db_query_prepare import create_materialized_views
from app.db_session.db_query_prepare import create_db_if_not_exists

app = FastAPI(title="Streamfinity API CQRS", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(token.router)
app.include_router(movies_and_actors.router)


@app.on_event("startup")
def on_startup() -> None:
    create_db_if_not_exists()
    SQLModel.metadata.create_all(db_engine.engine)
    fill_db_with_data_if_empty()
    remove_duplicate_links()
    create_materialized_views()


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
