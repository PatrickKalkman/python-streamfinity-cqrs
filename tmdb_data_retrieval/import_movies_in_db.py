import time
from sqlmodel import Session, SQLModel, create_engine, Field, Relationship
from typing import Any, Generator, Optional
import json

database_url = "mssql+pyodbc://sa:Password123@localhost/streamfinity?&driver=ODBC Driver 18 for SQL Server&Encrypt=no"

engine = create_engine(
    database_url,
    echo=False,
    connect_args={"check_same_thread": False}
)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


class MovieActorLink(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", default=None)
    actor_id: int = Field(foreign_key="actor.id", default=None)


class Movie(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    length: int
    synopsis: str
    release_date: str
    director: str
    genre: str
    tmdb_id: int
    rating: Optional[float] = None
    actors: list["Actor"] = Relationship(back_populates="movies", link_model=MovieActorLink)


class Actor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    date_of_birth: Optional[str] = None
    tmdb_id: int
    character: str
    gender: int
    movies: list[Movie] = Relationship(back_populates="actors", link_model=MovieActorLink)


# Start timing
start_time = time.time()

# Load the data from the file
with open('./cache/all_action_movies_with_cast_data_2022.json', 'r') as f:
    all_data = json.load(f)

with Session(engine) as session:
    # Loop over all movies
    for movie_data in all_data:
        genre_str = ','.join(str(genre_id) for genre_id in movie_data['genre_ids'])

        movie = Movie(
            title=movie_data['title'],
            length=0,
            synopsis=movie_data['overview'],
            release_date=movie_data['release_date'],
            tmdb_id=movie_data['id'],
            director='',
            genre=genre_str,
            rating=movie_data['vote_average'] if 'vote_average' in movie_data else None
        )

        # Insert the movie into the database
        session.add(movie)
        session.commit()

        # Loop over all actors in the movie
        actors = []
        actor_links = []
        for actor_data in movie_data['cast']:
            if actor_data['known_for_department'] == 'Acting':
                actor = Actor(
                    name=actor_data['name'],
                    date_of_birth='',
                    tmdb_id=actor_data['id'],
                    character=actor_data['character'],
                    gender=actor_data['gender']
                )
                actors.append(actor)

                # Add link between movie and actor
                actor_link = MovieActorLink(movie_id=movie.id, actor_id=actor.id)
                actor_links.append(actor_link)

        # Bulk insert actors and movie-actor links
        session.bulk_save_objects(actors)
        session.bulk_save_objects(actor_links)

        session.commit()

# End timing
end_time = time.time()

print(f"Time taken: {end_time - start_time} seconds")
