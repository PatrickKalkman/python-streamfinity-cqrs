import time
from sqlmodel import Session
from loguru import logger

import json

from app.schemas.movie_actor_schema import Movie, Actor, MovieActorLink
from app.db_session.db_engine import engine


def fill_db_with_data_if_empty():
    # Check if movies are already imported
    with Session(engine) as session:
        if session.query(Movie).count() > 0:
            logger.info("Movies already imported in the database. Skipping import.")
            return

    logger.info("No movies found in the database. Importing movies from TMDB cache.")
    # Start timing
    start_time = time.time()

    # Load the data from the file
    with open('./tmdb_data_retrieval/cache/all_action_movies_with_cast_data_2022.json',
              'r') as f:
        all_data = json.load(f)

    with Session(engine) as session:
        # Collect all unique actors
        all_actors = []
        for movie_data in all_data:
            for actor_data in movie_data['cast']:
                if actor_data['known_for_department'] == 'Acting':
                    if actor_data['id'] not in [actor.tmdb_id for actor in all_actors]:
                        actor = Actor(
                            name=actor_data['name'],
                            date_of_birth='',
                            tmdb_id=actor_data['id'],
                            character=actor_data['character'],
                            gender=actor_data['gender']
                        )
                        all_actors.append(actor)

        # Bulk insert actors
        session.bulk_save_objects(all_actors)
        session.commit()

        # Fetch all actors from the DB into a dictionary
        actors_dict = {actor.tmdb_id: actor for actor in session.query(Actor)}

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
                rating=movie_data['vote_average'] if 'vote_average' in movie_data
                else None
            )

            # Insert the movie into the database
            session.add(movie)
            session.commit()

            # Loop over all actors in the movie
            actor_links = []
            for actor_data in movie_data['cast']:
                if actor_data['known_for_department'] == 'Acting':
                    # Get actor from the dictionary
                    actor = actors_dict[actor_data['id']]

                    # Add link between movie and actor
                    assert (movie.id is not None)
                    actor_link = MovieActorLink(movie_id=movie.id, actor_id=actor.id)
                    actor_links.append(actor_link)

            # Bulk insert movie-actor links
            session.bulk_save_objects(actor_links)
            session.commit()

    # End timing
    end_time = time.time()

    logger.info(f"Movies imported in: {end_time - start_time} seconds")
