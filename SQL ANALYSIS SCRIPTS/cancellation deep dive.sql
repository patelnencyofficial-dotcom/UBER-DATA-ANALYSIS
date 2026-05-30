-- ---------------------------------------------------------(1).	What is the overall cancellation rate, and what percentage are cancelled by driver vs rider?
 -- Overall cancellation rate
SELECT
    COUNT(c.cancel_id)                          AS total_cancellations,
    ROUND(COUNT(c.cancel_id) * 100.0 /
        (SELECT COUNT(*) FROM trips), 2)        AS overall_cancel_rate_pct
FROM cancellations AS c;

-- By driver vs rider
SELECT
    c.cancelled_by,
    COUNT(c.cancel_id)                          AS cancelled_trips,
    ROUND(COUNT(c.cancel_id) * 100.0 /
        (SELECT COUNT(*) FROM trips), 2)        AS cancellation_rate_pct
FROM cancellations AS c
GROUP BY c.cancelled_by
ORDER BY cancelled_trips DESC;
 

-- ------------------------------------------------------------(2). 	What are the top 5 cancellation reasons, separately for drivers and riders?
 WITH ranked_reasons AS (
    SELECT
        CASE WHEN cancelled_by = 'rider' 
             THEN 'Rider' 
             ELSE 'Driver' 
        END                             AS cancelled_by,
        reason,
        COUNT(*)                        AS total_cancellations,
        RANK() OVER (
            PARTITION BY cancelled_by
            ORDER BY COUNT(*) DESC
        )                               AS reason_rank
    FROM cancellations
    GROUP BY cancelled_by, reason
)
SELECT
    cancelled_by,
    reason,
    total_cancellations,
    reason_rank
FROM ranked_reasons
WHERE reason_rank <= 5
ORDER BY cancelled_by, reason_rank;


-- ---------------------(3).	Do drivers with lower ratings cancel more frequently? Compare cancellation rate by driver rating bucket.
 SELECT 
    CASE
        WHEN d.rating BETWEEN 1.0 AND 3 THEN 'Low Rated'
        WHEN d.rating BETWEEN 3   AND 4 THEN 'Moderate'
        WHEN d.rating BETWEEN 4   AND 5 THEN 'High Rated'
    END AS rating_bucket,
    
    COUNT(DISTINCT t.trip_id)  AS total_trips,
    COUNT(DISTINCT c.cancel_id) AS cancelled_trips,
    
    ROUND(
    COUNT(DISTINCT c.cancel_id) * 100.0 / COUNT(t.trip_id)
, 2) AS cancellation_rate_pct

FROM drivers d
JOIN trips t        ON d.driver_id = t.driver_id
LEFT JOIN cancellations c ON t.trip_id = c.trip_id   -- LEFT JOIN keeps non-cancelled trips too

GROUP BY rating_bucket
ORDER BY cancellation_rate_pct DESC;


-- 4.	At what time of day do cancellations peak — are late-night cancellations higher than daytime?

select
hour(cancelled_at) as hour,
count(cancel_id) as total_cancelled_trips,
count(cancel_id) * 100 / (select count(*) from cancellations) as cancel_pct,
rank() over(order by count(cancel_id) desc) as hour_rank

from  cancellations
group by hour(cancelled_at)
ORDER BY hour_rank;



-- 5.	Which riders have cancelled more than 3 trips — identify repeat cancellers?

 SELECT
    r.rider_id,
    u.name,
    u.email,
    u.phone,
    u.city,
    COUNT(c.cancel_id)                                    AS total_cancellations,
    ROUND(COUNT(c.cancel_id) * 100.0 / 
    (SELECT COUNT(*) FROM cancellations), 2)              AS pct_of_all_cancels,
    RANK() OVER (ORDER BY COUNT(c.cancel_id) DESC)        AS cancel_rank

FROM cancellations c
JOIN trips t   ON c.trip_id   = t.trip_id
JOIN riders r  ON t.rider_id  = r.rider_id
JOIN users u   ON r.user_id   = u.user_id    --  added to get name, email, city

GROUP BY r.rider_id, u.name, u.email, u.phone, u.city
HAVING COUNT(c.cancel_id) > 3

ORDER BY total_cancellations DESC;



