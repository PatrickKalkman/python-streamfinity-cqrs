from sqlmodel import SQLModel


class MovieWithActors(SQLModel, table="vMovieWithActors"):
    movie_id: int
    title: str
    length: int
    synopsis: str
    release_date: str
    director: str
    genre: str
    rating: float
    actor_id: int
    name: str
    date_of_birth: str
    character: str
    gender: int
