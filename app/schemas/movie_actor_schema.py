from typing import List
from sqlmodel import Field, Relationship, SQLModel


class MovieInput(SQLModel):
    title: str
    length: int
    synopsis: str
    release_date: str
    director: str
    genre: str
    tmdb_id: int
    rating: float | None = None


class MovieActorLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", default=None)
    actor_id: int = Field(foreign_key="actor.id", default=None)


class Movie(MovieInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    actors: list["Actor"] = Relationship(back_populates="movies",
                                         link_model=MovieActorLink)


class MovieOutput(MovieInput):
    id: int
    actors: list["Actor"] = []


class ActorInput(SQLModel):
    name: str
    date_of_birth: str
    tmdb_id: int
    character: str
    gender: int


class Actor(ActorInput, table=True):
    id: int | None = Field(primary_key=True, default=None)
    movies: list[Movie] = Relationship(back_populates="actors",
                                       link_model=MovieActorLink)


class ActorBase(SQLModel):
    id: int
    name: str
    date_of_birth: str
    tmdb_id: int
    character: str
    gender: int


class MovieOut(MovieInput, table=False):
    actors: List[ActorBase]
