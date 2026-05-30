-- ------------------------------------------------(1).	What is the average review rating given by riders to drivers, and by drivers to riders?
SELECT
    CASE 
        WHEN u.is_driver = 0 THEN 'Rider -->  Driver'
        WHEN u.is_driver = 1 THEN 'Driver --> Rider'
    END                          AS review_direction,
    ROUND(AVG(r.rating), 2)      AS avg_rating,
    COUNT(*)                     AS total_reviews
FROM reviews AS r
JOIN users AS u ON r.reviewer_id = u.user_id
GROUP BY u.is_driver;
 


-- --------------------------------------------(2).	Which drivers have the lowest average review scores (from riders) across at least 5 reviews?

SELECT
    d.driver_id,
    u.name                          AS driver_name,
    ROUND(AVG(rv.rating), 2)        AS avg_rating,
    COUNT(rv.review_id)             AS total_reviews,
    RANK() OVER (
        ORDER BY AVG(rv.rating) ASC 
    )                               AS rating_rank
FROM reviews AS rv
JOIN users AS reviewer  ON rv.reviewer_id = reviewer.user_id
JOIN users AS u         ON rv.reviewee_id = u.user_id
JOIN drivers AS d       ON u.user_id      = d.user_id
WHERE reviewer.is_driver = 0          -- only reviews FROM riders
GROUP BY d.driver_id, u.name
HAVING COUNT(rv.review_id) >= 5       -- at least 5 reviews
ORDER BY avg_rating ASC;
 
 
--  ----------------------------------------------(3).	Is there a relationship between trip fare and review rating — do expensive trips get better reviews?
select 
min(total_fare/distance_km),
max(total_fare/distance_km),
avg (total_fare/distance_km)
from trips;

SELECT
    CASE
        WHEN t.total_fare / t.distance_km < 5        THEN '1. Cheap (< 5/km)'
        WHEN t.total_fare / t.distance_km < 15       THEN '2. Moderate (5–15/km)'
        WHEN t.total_fare / t.distance_km >= 15      THEN '3. Expensive (≥ 15/km)'
        ELSE                                               'Uncategorized'
    END                               AS fare_bucket,

    COUNT(DISTINCT t.trip_id)         AS trip_count,
    ROUND(AVG(t.total_fare), 2)       AS avg_fare,
    ROUND(AVG(t.distance_km), 2)      AS avg_distance_km,
    ROUND(AVG(t.total_fare / t.distance_km), 2) AS avg_fare_per_km,
    ROUND(AVG(r.rating), 2)           AS avg_rider_rating   -- rider → driver only

FROM trips AS t
JOIN reviews AS r       ON t.trip_id     = r.trip_id
JOIN users   AS reviewer ON r.reviewer_id = reviewer.user_id

WHERE t.status          = 'completed'
  AND reviewer.is_driver = 0            -- only ratings given BY riders

GROUP BY fare_bucket
ORDER BY fare_bucket;




-- --------------------------------------------(4).	What percentage of completed trips result in a review being left — what is the review submission rate?
SELECT
    COUNT(DISTINCT t.trip_id)                        AS completed_trips,
    COUNT(DISTINCT r.trip_id)                        AS trips_with_review,
    COUNT(DISTINCT t.trip_id) - 
    COUNT(DISTINCT r.trip_id)                        AS trips_without_review,
    ROUND(
        COUNT(DISTINCT r.trip_id) * 100.0 /
        COUNT(DISTINCT t.trip_id), 2
    )                                                AS review_submission_rate_pct

FROM trips AS t
LEFT JOIN reviews AS r ON t.trip_id = r.trip_id
WHERE t.status = 'completed';

 