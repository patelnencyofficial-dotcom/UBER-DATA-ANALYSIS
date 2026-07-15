-- -------------------------------------(1)------Who are the top 10 riders by total spend (lifetime value) and total trips taken?
SELECT 
    r.rider_id AS riders,
    ROUND(SUM(t.total_fare), 2) AS total_spend,
    r.total_trips
FROM
    trips AS t
        INNER JOIN
    riders AS r ON t.rider_id = r.rider_id
WHERE
    t.status = 'completed'
GROUP BY r.rider_id
ORDER BY total_spend DESC
LIMIT 10;
 
--  ------------------------------(2).	Segment riders into 3 groups — low (1–5 trips), medium (6–20 trips), high (20+ trips). What % of revenue does each contribute?
with trip_groups as (
select 
r.rider_id,
t.total_fare,
r.total_trips,
case when r.total_trips between 11 and 30 then "MEDIUM (11-30)"
WHEN r.total_trips > 30 then "HIGH( 40+)" ELSE "LOW( <10)" end as segment

from riders as r 
inner join trips as t 
on r. rider_id = t.rider_id 
where t.status = "completed" )

select 
segment,
count(distinct rider_id) as riders, 
sum(total_trips) as toatl_trips,
round(sum(total_fare),2) as total_revenue,
round(sum(total_fare) * 100 / (select sum(total_fare) from trip_groups ),2) as pct_total_revenue
from trip_groups
group by segment ;

 
 

-- ------------------------------------------------(3) What is the distribution of rider ratings? How many riders have a rating below 4.0?
SELECT 
    CASE
        WHEN rating BETWEEN 1.0 AND 1.5 THEN '1.0 - 1.5'
        WHEN rating BETWEEN 1.5 AND 2.0 THEN '1.5 - 2.0'
        WHEN rating BETWEEN 2.0 AND 2.5 THEN '2.0 - 2.5'
        WHEN rating BETWEEN 2.5 AND 3.0 THEN '2.5 - 3.0'
        WHEN rating BETWEEN 3.0 AND 3.5 THEN '3.0 - 3.5'
        WHEN rating BETWEEN 3.5 AND 4.0 THEN '3.5 - 4.0'
        WHEN rating BETWEEN 4.0 AND 4.5 THEN '4.0 - 4.5'
        WHEN rating BETWEEN 4.5 AND 5.0 THEN '4.5 - 5.0'
    END AS rating_bucket,
    COUNT(rider_id) AS riders,
    ROUND(COUNT(rider_id) * 100 / (SELECT 
                    COUNT(*)
                FROM
                    riders),
            2) AS percentage
FROM
    riders
GROUP BY rating_bucket
ORDER BY MIN(rating)
-- ---------------------(below 4.0 rated riders )  50 percent----------------


SELECT
    COUNT(*)                                        AS riders_below_4,
    ROUND(COUNT(*) * 100.0 / 
         (SELECT COUNT(*) FROM riders 
          WHERE rating IS NOT NULL), 2)             AS pct_below_4
FROM riders
WHERE rating < 4.0
AND rating IS NOT NULL;




-- --------------------------------------------(4).	How many new riders joined each month — what does the rider acquisition trend look like?-------------

select
date_format(created_at, "%-%m")                   as months,
count(distinct rider_id)                           as New_riders,
lag(count(distinct rider_id)) over (order by date_format(created_at, "%y-%m"))                                      as previous_month_riders,
round(count(distinct rider_id) -  lag(count(distinct rider_id)) over (order by date_format(created_at, "%y-%m")))   as mom_change,
(count(distinct rider_id) -  lag(count(distinct rider_id)) over (order by date_format(created_at, "%y-%m")) )    * 100 / 
(lag(count(distinct rider_id)) over (order by date_format(created_at, "%y-%m")))                                    as pct_change,

sum(count(rider_id)) over(order by date_format(created_at, "%y-%m")) as cummilative_riders
from riders
group by date_format(created_at, "%y-%m");









-- ----------------------------(5).	What is the average time gap between a rider's first trip and their second trip (early retention signal)?----------------------------



WITH numbered_trips AS (
    SELECT
        rider_id,
        started_at,
        ROW_NUMBER() OVER (
            PARTITION BY rider_id 
            ORDER BY started_at
        )                           AS trip_number
    FROM trips
    WHERE status = 'completed'
    AND started_at IS NOT NULL
),
first_second_trips AS (
    SELECT
        rider_id,
        MAX(CASE WHEN trip_number = 1 
            THEN started_at END)    AS first_trip,
        MAX(CASE WHEN trip_number = 2 
            THEN started_at END)    AS second_trip
    FROM numbered_trips
    WHERE trip_number IN (1, 2)
    GROUP BY rider_id
)
SELECT
    COUNT(rider_id)                             AS total_riders_analysed,
    ROUND(AVG(TIMESTAMPDIFF(DAY, 
          first_trip, second_trip)), 2)         AS avg_days_to_second_trip,
    MIN(TIMESTAMPDIFF(DAY, 
          first_trip, second_trip))             AS min_days,
    MAX(TIMESTAMPDIFF(DAY, 
          first_trip, second_trip))             AS max_days,
    ROUND(STDDEV(TIMESTAMPDIFF(DAY, 
          first_trip, second_trip)), 2)         AS stddev_days
FROM first_second_trips
WHERE second_trip IS NOT NULL;

-- (((((((((((((((((((------------------GROUP BY collapses many rows into one.
--                                      -CASE WHEN leaves one real value and the rest are NULLs.
--                                      -MAX() just picks the real value and ignores the NULLs.






-- ---------------------------------------------(6).	Which cities have the highest average rider spend per trip?-------------------------------------------
select 
city,
count(t.trip_id) as total_trips,
round(sum(t.total_fare)) as rider_spent,
round(avg(t.total_fare)) as avg_rider_spent,
rank() over(order by avg(t.total_fare) desc) as city_rank
from locations as l 
join trips as t 
on l.location_id = t.dropoff_location_id
where status = "completed"
group by city
order by avg_rider_spent desc; 


 