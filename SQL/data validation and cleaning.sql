 #--------check for null values ------
        
select * from cancellations
where 
trip_id is null 
or cancelled_by is null
or cancel_id is null 
or reason is null
or cancelled_at is null;


SELECT * 
FROM users
WHERE user_id IS NULL
   OR name IS NULL
   OR email IS NULL;
   
SELECT * 
FROM riders
WHERE rider_id IS NULL
   OR user_id IS NULL;


SELECT * 
FROM drivers
WHERE driver_id IS NULL
   OR user_id IS NULL;
   
SELECT * 
FROM trips
WHERE trip_id IS NULL
   OR rider_id IS NULL
   OR driver_id IS NULL
   OR pickup_location_id IS NULL
   OR dropoff_location_id IS NULL
   OR status IS NULL
   OR requested_at IS NULL;
   
SELECT * 
FROM payments
WHERE payment_id IS NULL
   OR trip_id IS NULL
   OR amount IS NULL
   OR status IS NULL;
   
SELECT * 
FROM locations
WHERE location_id IS NULL
   OR zone_name IS NULL
   OR city IS NULL;


SELECT * 
FROM reviews
WHERE review_id IS NULL
   OR trip_id IS NULL
   OR reviewer_id IS NULL
   OR reviewee_id IS NULL
   OR rating IS NULL;
   
   
   
   




#----------foriegn key validation through left join------------

select * from cancellations as c 
left join  trips as t
on c.trip_id = t.trip_id
where t.trip_id is null ;


select * from  drivers as d
left join users as u
on d.user_id = u.user_id
where u.user_id is null ;

select * from payments as p 
left join trips as t
on p.trip_id = t.trip_id
where t.trip_id is null;

select * from reviews as r 
left join trips as t
on r.trip_id = t.trip_id
where t.trip_id is null ;

select * from riders as r
left join users as u
on r.user_id = u.user_id 
where u.user_id is null;

select * from trips as t
left join  riders as r
on t.rider_id = r.rider_id
where r.rider_id is null;

select * from  trips as t 
left join drivers as d
 on  t.driver_id = d.driver_id
 where d.driver_id is null;

