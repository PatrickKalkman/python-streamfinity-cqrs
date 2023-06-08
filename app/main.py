import uvicorn
from fastapi import FastAPI
from sqlmodel import SQLModel

import db_session.db_engine as db_engine
from routers import actors, movies, subscriptions, token, users

app = FastAPI(title="Streamfinity API CQRS", version="0.1.0")
app.include_router(movies.router)
app.include_router(actors.router)
app.include_router(subscriptions.router)
app.include_router(users.router)
app.include_router(token.router)


@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(db_engine.engine)


if __name__ == "__main__":
    uvicorn.run(app, reload=True)
