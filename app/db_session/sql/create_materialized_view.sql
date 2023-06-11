CREATE VIEW vMovieWithActors
  WITH SCHEMABINDING
  AS
    SELECT m.id as movie_id, 
           m.title, 
           m.length, 
           m.synopsis, 
           m.release_date, 
           m.director, 
           m.genre, 
           m.rating, 
           a.id as actor_id, 
           a.name, 
           a.date_of_birth,
           a.character,
           a.gender
    FROM dbo.Movie m
      JOIN dbo.MovieActorLink mal ON m.id = mal.movie_id
      JOIN dbo.Actor a ON a.id = mal.actor_id