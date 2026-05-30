
#--------------total trips per day--------
SELECT 
    DATE( completed_at) AS trip_date,
    COUNT(*) AS total_trips
FROM trips
WHERE status = 'completed'
GROUP BY DATE(completed_at)
ORDER BY trip_date;




#------------total trips per month------(datafromat will convert the date column into year/month format)
select 
 date_format(completed_at, '%Y-%m') as month ,
 count(*) as monthy_trips
 from trips
 where status = "completed"
 group by month
 order by month;
 
  #----------------year plus monthly trips ----------------
  SELECT 
    YEAR(completed_at) AS year,
    MONTH(completed_at) AS month,
    COUNT(*) AS total_trips
FROM trips
WHERE status = 'completed'
GROUP BY year, month
ORDER BY year, month;


#----------hourly trips ---(to find the peak booking hours not very useful)-------
SELECT 
    HOUR(completed_at) AS hour,
    COUNT(*) AS total_trips
FROM trips
WHERE status = 'completed'
GROUP BY hour
ORDER BY hour;

#-------------revenue ------------------
  SELECT 
    YEAR(completed_at) AS year,
    MONTH(completed_at) AS month,
    COUNT(*) AS total_trips,
    round(sum(total_fare)) as monthly_revenue
FROM trips
WHERE status = 'completed'
GROUP BY year, month
ORDER BY year, month;

#---------------------------------------RIDER ANALYSIS--------------------------------------------
# total trips per rider
SELECT rider_id, count(trip_id) as total_rider_trips
from trips
where status = "completed"
group by rider_id ;

# active riders
SELECT rider_id, count(trip_id) as  active 
from trips 
where status = "completed"
group by rider_id 
having count(trip_id) > 50  ;

# old vs new rider
select rider_id, year(created_at) as active_year,
case when year(created_at) > 2023 then "NEW" ELSE "OLD"
END as rider_type  
from riders;

#__________ rider value  
#total spending per rider
SELECT rider_id,  round(sum(total_fare)) as total_value
from trips
where status = "completed"
group by rider_id ;

# top 10 high performing riders
SELECT rider_id, round(sum(total_fare)) as total_value
from trips
group by rider_id
order by round(sum(total_fare)) desc limit 10
 ;
 
# high valued vs low valued customers
SELECT  rider_id,
case when (sum(total_fare)) > 1500 then "HIGH VALUED" else "LOW VALUED"  END AS "VALUE STATUS"
from trips
where status = "completed"
group by rider_id ;



#-----------------------------------------drivers analysis-----------------------------------------
#Trips per driver with earnings
select driver_id , count(trip_id) as "total trips", sum(total_fare) as "total earnings"
from trips 
where status="completed"
group by driver_id;

#Active vs inactive drivers 
select driver_id, case when is_active = 1 then "ACTIVE" else "INACTIVE" end as "active status"
from drivers 
order by is_active;

# count the active and inactive drivers
select is_active, count(is_active)
from drivers 
group by is_active ;

#ratings (drivers + reviews) 
select driver_id , rating
from drivers
group by driver_id;

#Average driver rating 
select driver_id , round(avg(rating),2)
from drivers
group by driver_id;

#High vs low rated drivers 
select driver_id , round(avg(rating),2) as average_rating
from drivers
where rating > 4.5
group by driver_id
order by rating desc;

select driver_id , round(avg(rating),2) as average_rating
from drivers
where rating < 3
group by driver_id
order by rating desc;
#------------------------------------------location analysis-------------------------------------
#Most popular pickup zones 
-- STEP 9A: Most Popular Pickup Zones  (since we dont have the tripid in location table to count  we will join the locationid from locations and pickupid at trips )

SELECT l.zone_name, l.city, l.zone_type,
    COUNT(t.trip_id) AS total_pickups
FROM trips t
JOIN locations l
    ON t.pickup_location_id = l.location_id
GROUP BY l.zone_name, l.city, l.zone_type
ORDER BY total_pickups DESC;
-- --"""
-- Most common routes 


-- Trips by city 
-- Revenue by city """
