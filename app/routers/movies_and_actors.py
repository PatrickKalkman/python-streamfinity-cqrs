from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from sqlalchemy import text

from app.db_session.db_engine import get_session
from app.schemas.movie_and_actors_schema import MovieWithActors
from app.schemas.params_schema import PaginationParams


router = APIRouter(prefix="/api/movies_and_actors")


@router.get("/")
def get_movies_with_actors(
    params: PaginationParams = Depends(),
    session: Session = Depends(get_session)
) -> List[MovieWithActors]:
    with session.begin():
        query = (f"SELECT * FROM vMovieWithActors ORDER BY movie_id OFFSET {params.skip}"
                 f" ROWS FETCH NEXT {params.limit} ROWS ONLY")
        result = session.execute(text(query))
        movies = [MovieWithActors(**dict(row)) for row in result.fetchall()]
    return movies
