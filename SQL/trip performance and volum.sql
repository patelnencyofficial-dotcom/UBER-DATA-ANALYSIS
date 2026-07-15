-- -------------------------------(1)   What is the total number of trips and what percentage are completed vs cancelled vs other statuses?
SELECT 
    status AS trip_status,
    COUNT(*) AS total_trips,
    ROUND(COUNT(*) * 100.0 / (SELECT 
                    COUNT(*)
                FROM
                    trips),
            2) AS percentage
FROM
    trips
GROUP BY status;
 
-- ----------------------------------(2)           What is the average, minimum, maximum, and standard deviation of trip distance (km)?

SELECT 
    ROUND(AVG(distance_km), 2) AS 'average trip distance(KM)',
    ROUND(MIN(distance_km), 2) AS 'minimum trip distance(KM)',
    ROUND(MAX(distance_km), 2) AS 'maximum trip distance(KM)',
    ROUND(STDDEV(distance_km), 2) AS 'standard deviation(KM) '
FROM
    trips
WHERE
    status = 'completed'
        AND distance_km IS NOT NULL;

-- -----------------------------------------------(3)   What is the average, minimum, and maximum trip duration in minutes?
SELECT 
    ROUND(AVG(duration_mins), 2) AS 'average trip duration(mins)',
    ROUND(MIN(duration_mins), 2) AS 'shortest trip duration(mins)',
    ROUND(MAX(duration_mins), 2) AS 'longest trip duration (mins)',
    ROUND(STDDEV(duration_mins), 2) AS 'standard deviation'
FROM
    trips
WHERE
    status = 'completed'
        AND duration_mins IS NOT NULL;

-- ------------------------------------------(4)  What is the average wait time (time from requested_at to started_at) per trip?

SELECT 
    ROUND(AVG(TIMESTAMPDIFF(MINUTE,
                requested_at,
                started_at))) AS 'average waiting time(minutes)'
FROM
    trips
WHERE
    status = 'completed'
        AND requested_at IS NOT NULL
        AND started_at IS NOT NULL;
 

-- -----------------------------------------(5)  How many trips happen each hour of the day? Which 3 hours have the highest volume?

select 
hour(started_at) as hours,
count(*) as "total trips per hour",
ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM trips), 2) AS percentage,
rank() over(order by count(*) desc) as "volume rank",
   case when rank() over(order by count(*) desc)  <=3 then "peak hour" else " " end as peak_status
from trips
group by hour(started_at)
order by count(*) desc;

 

-- -------------------------------------------------------(6) does trip volume differ by day of the week (Monday through Sunday)?

SELECT 
    DAYNAME(started_at) AS day_of_week,
    COUNT(*) AS total_trips,
    ROUND(COUNT(*) * 100.0 / (SELECT 
                    COUNT(*)
                FROM
                    trips),
            2) AS percentage,
    ROUND(AVG(total_fare), 2) AS avg_fare,
    ROUND(AVG(distance_km), 2) AS avg_distance_km
FROM
    trips
WHERE
    started_at IS NOT NULL
GROUP BY DAYNAME(started_at) , DAYOFWEEK(started_at)
ORDER BY DAYOFWEEK(started_at);

-- ---------------------------------------------------(7)  How has monthly trip volume trended over time — is it growing, declining, or flat?
select 
date_format(started_at, "%y-%m") as months ,
count(*) as total_trips ,
lag(count(*)) over(order by date_format(started_at, "%y-%m")) as pervious_month_trips ,
count(*) - lag(count(*)) over(order by date_format(started_at, "%y-%m")) as monthly_change,
round((count(*) - lag(count(*)) over(order by date_format(started_at, "%y-%m")))*100 / (lag(count(*)) over(order by date_format(started_at, "%y-%m"))) ,2) as change_pct
from trips as mothly_change_in_percent
group by date_format(started_at, "%y-%m");



-- ------------------------------------------------(8)What proportion of trips use surge pricing (surge_multiplier > 1), and what is the average surge level?
-- ------------------------------(Surge is Uber's primary revenue lever. High surge usage means high demand but can also mean rider dissatisfaction.)

SELECT 
    COUNT(CASE
        WHEN surge_multiplier > 1 THEN 1
    END) AS surge_trips,
    ROUND(COUNT(CASE
                WHEN surge_multiplier > 1 THEN 1
            END) * 100 / COUNT(*),
            2) AS surge_percentage,
    ROUND(AVG(CASE
                WHEN surge_multiplier > 1 THEN surge_multiplier
            END),
            2) AS 'surge level'
FROM
    trips
WHERE
    status = 'completed'




