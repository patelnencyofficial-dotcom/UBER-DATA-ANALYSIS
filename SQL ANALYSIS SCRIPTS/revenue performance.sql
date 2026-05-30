-- -----------------------------------------------------(1)What is the total revenue, average fare per trip, and revenue per km?-----------------------------
SELECT 
    ROUND(SUM(total_fare), 2) AS total_revenue,
    ROUND(SUM(distance_km), 2) AS total_distance,
    ROUND(AVG(total_fare), 2) AS average_fare,
    ROUND(AVG(distance_km)) AS avg_km,
    ROUND(SUM(total_fare) / SUM(distance_km), 2) AS revenue_per_km
FROM
    trips
WHERE
    status = 'completed'
        AND total_fare IS NOT NULL
        AND distance_km IS NOT NULL
;

-- -----------------------------------------(2)    How does total revenue and average fare change month over month?---------------------------------------
SELECT 
    DATE_FORMAT(started_at, '%Y-%m')         AS month,
    ROUND(SUM(total_fare), 2)                AS monthly_revenue,
    ROUND(AVG(total_fare), 2)                AS avg_monthly_revenue,
    ROUND(LAG(SUM(total_fare)) 
          OVER (ORDER BY DATE_FORMAT(started_at, '%Y-%m')), 2)     AS previous_month_rev,
    ROUND(SUM(total_fare) - LAG(SUM(total_fare)) 
          OVER (ORDER BY DATE_FORMAT(started_at, '%Y-%m')), 2)     AS revenue_change,
    ROUND((SUM(total_fare) - LAG(SUM(total_fare)) 
          OVER (ORDER BY DATE_FORMAT(started_at, '%Y-%m'))) * 100.0 / 
          LAG(SUM(total_fare)) 
          OVER (ORDER BY DATE_FORMAT(started_at, '%Y-%m')), 2)            AS revenue_growth_pct
FROM trips
WHERE status = 'completed'
AND total_fare IS NOT NULL
AND started_at IS NOT NULL
GROUP BY DATE_FORMAT(started_at, '%Y-%m')
ORDER BY month;

-- ------------------------------------------(3) does average fare and trip count differ between No Surge, Low Surge (1–1.5x), and High Surge (>1.5x) tiers?
SELECT 
    CASE
        WHEN surge_multiplier = 1 THEN 'No surge'
        WHEN surge_multiplier BETWEEN 1 AND 1.5 THEN 'Low surge (1.0-1.5x)'
        ELSE 'High surge (1.5x+)'
    END AS surge_tier,
    COUNT(*) AS total_trips,
    ROUND(AVG(total_fare), 2) AS avg_fare,
    ROUND(SUM(total_fare), 2) AS total_revenue,
    ROUND(COUNT(*) * 100.0 / (SELECT 
                    COUNT(*)
                FROM
                    trips
                WHERE
                    status = 'completed'),
            2) AS trip_percentage
FROM
    trips
WHERE
    status = 'completed'
        AND surge_multiplier IS NOT NULL
GROUP BY CASE
    WHEN surge_multiplier = 1 THEN 'No surge'
    WHEN surge_multiplier BETWEEN 1 AND 1.5 THEN 'Low surge (1.0-1.5x)'
    ELSE 'High surge (1.5x+)'
END
ORDER BY MIN(surge_multiplier)



-- --------------------------------------- (4)What is the fare distribution — create 5 buckets (e.g. under $10, $10–25, $25–50, $50–100, over $100)?
SELECT 
    CASE
        WHEN total_fare < 10 THEN 'under $10'
        WHEN total_fare BETWEEN 10 AND 25 THEN '$10-25'
        WHEN total_fare BETWEEN 25 AND 50 THEN '$25-50'
        WHEN total_fare BETWEEN 50 AND 100 THEN '$50-100'
        ELSE 'over $100'
    END AS trip_fare,
    COUNT(*) AS total_trips,
    ROUND(COUNT(*) * 100 / (SELECT 
                    COUNT(*)
                FROM
                    trips
                WHERE
                    status = 'completed'),
            2) AS trip_percentage,
    ROUND(AVG(total_fare), 2) AS avg_total_fare,
    ROUND(SUM(total_fare)) AS total_revenue,
    ROUND(SUM(total_fare) * 100 / (SELECT 
                    SUM(total_fare)
                FROM
                    trips
                WHERE
                    status = 'completed'),
            2) AS percentage
FROM
    trips
WHERE
    status = 'completed'
GROUP BY CASE
    WHEN total_fare < 10 THEN 'under $10'
    WHEN total_fare BETWEEN 10 AND 25 THEN '$10-25'
    WHEN total_fare BETWEEN 25 AND 50 THEN '$25-50'
    WHEN total_fare BETWEEN 50 AND 100 THEN '$50-100'
    ELSE 'over $100'
END
ORDER BY MIN(total_fare)

-- ----------------------------------------------------(5) Which hours of the day generate the highest total revenue (8)vs highest average fare(19)?  
select 
hour(started_at) as hour,
count(*) as total_trips,
sum(total_fare) as total_fare,
avg(total_fare) as avg_fare,
RANK() OVER (ORDER BY SUM(total_fare) DESC) AS revenue_rank,
RANK() OVER (ORDER BY AVG(total_fare) DESC) AS avg_fare_rank
from trips 
where status = "completed"
group by hour(started_at)
order by hour;


-- ---------------------------------------(6)What percentage of total revenue comes from the top 10% of trips by fare?
 WITH trip_buckets AS (
    SELECT 
        trip_id,
        total_fare,
        NTILE(10) OVER (ORDER BY total_fare DESC) AS bucket
    FROM trips 
    WHERE status = 'completed'
)
SELECT
    ROUND(SUM(CASE WHEN bucket = 1 
              THEN total_fare END))                AS top10_revenue,
    ROUND(SUM(CASE WHEN bucket = 1 
              THEN total_fare END) * 100.0 
              / SUM(total_fare), 2)                   AS top10_revenue_pct,
    COUNT(CASE WHEN bucket = 1 THEN 1 END)            AS top10_total_trips,
   round(sum(total_fare))  as total_fare,
   COUNT(*)                                          AS total_trips
FROM trip_buckets;



-- 	---------------------------------------------------(7)What is the revenue lost from cancelled trips (using base_fare of cancelled trips)?

SELECT 
    COUNT(*) AS total_cancelled_trips,
    ROUND(SUM(base_fare)) AS lost_revenue,
    ROUND(AVG(base_fare)) AS avg_lost_revenue
FROM
    trips AS t
        INNER JOIN
    cancellations AS c ON t.trip_id = c.trip_id
WHERE
    status = 'cancelled';
