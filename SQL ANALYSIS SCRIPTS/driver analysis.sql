-- Driver analysis
-- ------------------------------------(1) Who are the top 10 drivers by total trips completed and total earnings?-------------------------------------------
SELECT 
    driver_id, ROUND(SUM(total_fare), 2) AS total_earnings
FROM
    trips
WHERE
    status = 'completed'
GROUP BY driver_id
ORDER BY total_earnings DESC
LIMIT 10;


-- -----------------------------------(2)  What is the distribution of driver ratings — how many drivers fall in each 0.5-point bucket?

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
    COUNT(*) AS total_drivers,
    ROUND(COUNT(*) * 100 / (SELECT 
                    COUNT(*)
                FROM
                    drivers),
            2) AS percentage
FROM
    drivers
GROUP BY rating_bucket


--  ------------------------------------------------(3)  Do higher-rated drivers earn more per trip on average? Compare avg fare by driver rating bucket

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
    COUNT(*) AS total_drivers,
    ROUND(COUNT(*) * 100 / (SELECT 
                    COUNT(*)
                FROM
                    trips),
            2) AS percentage,
    ROUND(SUM(total_fare), 2) AS total_earnings,
    ROUND(AVG(total_fare), 2) AS avg_earnings
FROM
    drivers AS d
        INNER JOIN
    trips AS t ON d.driver_id = t.driver_id
WHERE
    t.status = 'completed'
GROUP BY rating_bucket
ORDER BY MIN(d.rating)


-- -------------------------------------------------(4)	What percentage of drivers are currently active (is_active = 1) vs inactive?-----------------------------
SELECT 
    CASE
        WHEN is_active = 1 THEN 'active'
        ELSE 'inactive'
    END AS active_status,
    COUNT(*) AS total,
    ROUND(COUNT(*) * 100 / (SELECT 
                    COUNT(*)
                FROM
                    drivers),
            2) AS percentage
FROM
    drivers
GROUP BY active_status


-- ----------------------------(5)  Which vehicle make and model is most common among drivers, and do vehicle types affect trip distance or fare?--------------------------

SELECT 
    d.vehicle_make AS brand,
    d.vehicle_model AS model,
    COUNT(*) AS total_trips,
    ROUND(SUM(t.total_fare), 2) AS total_fare,
    ROUND(AVG(t.total_fare), 2) AS avg_fare,
    ROUND(SUM(t.distance_km), 2) AS total_distance,
    ROUND(AVG(t.distance_km), 2) AS avg_distance_km,
    ROUND(AVG(t.duration_mins / t.distance_km), 2) AS avg_time_per_km
FROM
    trips AS t
        INNER JOIN
    drivers AS d ON t.driver_id = d.driver_id
WHERE
    t.status = 'completed'
        AND t.distance_km > 0
GROUP BY d.vehicle_make , d.vehicle_model
ORDER BY avg_fare DESC


-- ----------------------------------------(6).	How many trips does the average driver complete per month? What is the range (min–max)?-------------------------------------
with driver_monthly as(
select
d.driver_id ,
date_format(t.started_at,"%y-%m") as months,
count(*) as driver_trips
from trips as t
inner join drivers as d
on t.driver_id = d.driver_id
where t.status = "completed"
group by d.driver_id , date_format(started_at,"%y-%m"))

select 
round(avg(driver_trips)) as avg_trips_per_month_per_driver,
round(min(driver_trips)) as min_trips_per_month_per_driver,
round(max(driver_trips)) as max_trips_per_month_per_driver,
round(stddev(driver_trips),2) as stddev_trips_per_month_per_driver
from driver_monthly;


-- ----------------------------------------(7)	How long has each driver been on the platform (join_date to today), and does tenure correlate with rating or trips?
SELECT 
    d.driver_id,
    d.join_date,
    d.rating,
    count(t.trip_id) as total_trips,
    TIMESTAMPDIFF(MONTH,
        d.join_date,
        CURDATE()) AS months,
    TIMESTAMPDIFF(YEAR,
        d.join_date,
        CURDATE()) AS years,
	case when TIMESTAMPDIFF(YEAR,
        d.join_date,
        CURDATE()) < 2 THEN "NEW (UNDER 2 YEAR)"
        WHEN TIMESTAMPDIFF(YEAR,
        d.join_date,
        CURDATE()) < 3 THEN "INTERMEDIATE (UNDER 3 YEARS)"
        WHEN TIMESTAMPDIFF(YEAR,
        d.join_date,
        CURDATE()) < 5 THEN "EXPERIENCED" ELSE "VETERENE ( +5 YEARS )" END AS TENURE
FROM trips as t
inner join  drivers as d
   on t.driver_id = d.driver_id
WHERE
    is_active = 1
    group by driver_id, join_date, rating;

