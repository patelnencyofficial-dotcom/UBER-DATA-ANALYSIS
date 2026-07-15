-- -----------------------------------------------------(1).	Which pickup zones generate the most trips and the most total revenue?-----------------------------------
select 
l.zone_name,
count(t.trip_id) as total_trips,
round(avg(t.total_fare),2) as avg_fare,
round(sum(t.total_fare),2) as total_revenue,
rank() over(order by sum(t.total_fare) desc) as revenue_rank,
rank() over(order by sum(t.trip_id) desc) as trip_volume_rank

from locations as l 
join trips as t
on l.location_id = t.pickup_location_id
where t.status = "completed"
group by zone_name;


-- -------------------------------------------------(2).	Do trips from commercial zones have a higher average fare than residential or airport zones?
select 
l.zone_type,
count(t.trip_id) as total_trips,
round(avg(t.total_fare),2) as avg_fare,
round(sum(t.total_fare),2) as total_revenue,
rank() over(order by avg(t.total_fare) desc) as zone_rank

from locations as l 
join trips as t
on l.location_id = t.pickup_location_id
where t.status = "completed"
group by zone_type;


--  ------------------------------------------------(3).	What are the top 10 most common pickup-to-dropoff zone pairs (trip corridors)?--------------------------
SELECT 
    lp.zone_name                        AS pickup_zone,
    ld.zone_name                        AS dropoff_zone,
    COUNT(t.trip_id)                    AS total_trips,
    ROUND(AVG(t.total_fare), 2)         AS avg_fare,
    ROUND(SUM(t.total_fare), 2)         AS total_revenue
FROM trips AS t
JOIN locations AS lp
    ON t.pickup_location_id = lp.location_id
JOIN locations AS ld
    ON t.dropoff_location_id = ld.location_id
WHERE t.status = 'completed'
GROUP BY lp.zone_name, ld.zone_name
ORDER BY total_trips DESC
LIMIT 10; 


-- ----------------------------------------------(4).	Which dropoff zones have the longest average trip distance — indicating they are far from city centers?
 SELECT 
    l.zone_name                             AS dropoff_zone,
    l.zone_type,
    COUNT(t.trip_id)                        AS total_trips,
    ROUND(AVG(t.distance_km), 2)            AS avg_distance_km,
    ROUND(MAX(t.distance_km), 2)            AS max_distance_km,
    ROUND(MIN(t.distance_km), 2)            AS min_distance_km,
    RANK() OVER (
        ORDER BY AVG(t.distance_km) DESC
    )                                       AS distance_rank
FROM locations AS l
JOIN trips AS t
ON l.location_id = t.dropoff_location_id
WHERE t.status = 'completed'
GROUP BY l.zone_name, l.zone_type
ORDER BY distance_rank
LIMIT 10;

-- -----------------------------------------------------------(5).	Which zones have the highest cancellation rate for trips originating there?
SELECT 
    l.zone_name,
    l.zone_type,
    COUNT(t.trip_id)                            AS total_trips,
    SUM(CASE WHEN t.status = 'cancelled' 
        THEN 1 ELSE 0 END)                      AS cancelled_trips,
    ROUND(SUM(CASE WHEN t.status = 'cancelled' 
        THEN 1 ELSE 0 END) * 100.0 / 
        COUNT(t.trip_id), 2)                    AS cancellation_rate_pct,
    RANK() OVER (
        ORDER BY SUM(CASE WHEN t.status = 'cancelled' 
        THEN 1 ELSE 0 END) * 100.0 / 
        COUNT(t.trip_id) DESC
    )                                           AS cancel_rate_rank
FROM locations AS l
JOIN trips AS t
ON l.location_id = t.pickup_location_id
GROUP BY l.zone_name, l.zone_type
ORDER BY cancel_rate_rank
LIMIT 10;



