from sqlmodel import Session, SQLModel, create_engine, Field, Relationship
from typing import Any, Generator, Optional
import json

database_url = "mssql+pyodbc://sa:Password123@localhost/streamfinity?&driver=ODBC Driver 18 for SQL Server&Encrypt=no"

engine = create_engine(
    database_url,
    echo=True,
    connect_args={"check_same_thread": False}
)


def get_session() -> Generator[Session, Any, None]:
    with Session(engine) as session:
        yield session


class MovieActorLink(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    movie_id: int = Field(foreign_key="movie.id", primary_key=True, default=None)
    actor_id: int = Field(foreign_key="actor.id", primary_key=True, default=None)


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


# Insert a movie and its actors into the database
def insert_movie_actors(movie: Movie, actors: list[Actor], session: Session):
    # First add the movie
    session.add(movie)
    session.commit()

    # Then add all the actors
    for actor in actors:
        # Check if the actor is already in the database
        db_actor = session.get(Actor, actor.tmdb_id)

        # If not, add the actor
        if not db_actor:
            session.add(actor)
            session.commit()

        # Finally, add the link between the movie and the actor
        link = MovieActorLink(movie_id=movie.id, actor_id=actor.id)
        session.add(link)

    # Commit all changes
    session.commit()


# Load the data from the file
with open('./cache/all_action_movies_with_cast_data_2022.json', 'r') as f:
    all_data = json.load(f)

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

    # Loop over all actors in the movie
    actors = []
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

    # Insert the movie and its actors into the database
    print(f"Inserting movie {movie.title} and its actors")
    with Session(engine) as session:
        insert_movie_actors(movie, actors, session)
