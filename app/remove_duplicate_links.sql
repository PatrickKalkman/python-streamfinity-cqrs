WITH CTE AS(
   SELECT 
      [id],
      [movie_id],
      [actor_id],
      ROW_NUMBER() OVER(
            PARTITION BY [movie_id], [actor_id]
            ORDER BY [id]
      ) AS row_num
   FROM 
      [streamfinity].[dbo].[movieactorlink]
)
DELETE FROM CTE
WHERE row_num > 1
