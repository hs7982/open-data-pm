WITH LatestPollution AS (
    SELECT p.*
    FROM pollution p
    INNER JOIN (
        SELECT station_code, MAX(data_time) AS max_date_time
        FROM pollution
        GROUP BY station_code
    ) latest
    ON p.station_code = latest.station_code AND p.data_time = latest.max_date_time
)
SELECT 
    s.*,
    ST_X(s.location::geometry) as longitude,
    ST_Y(s.location::geometry) as latitude,
    p.*
FROM stations s
LEFT JOIN LatestPollution p
ON s.station_code = p.station_code
WHERE ST_DWithin(
    s.location,
    ST_SetSRID(ST_MakePoint(:longitude, :latitude), 4326)::geography,
    :radius
);