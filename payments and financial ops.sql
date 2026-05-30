-- --------------------------------------------------------(1).	What is the split of payment methods (wallet, card, cash) by transaction count and total amount?
select 
method,
count(payment_id) as total_transactions,
round(sum(amount),2) as total_amount,
round(sum(amount) * 100 / (select sum(amount) from payments ),2) as amount_pct
from payments 
where status = "success"
group by method; 

-- -----------------------------------------------------(2).	What is the payment failure rate per payment method? Which method fails most often?
select 
method,
count(payment_id) as total_transactions,
round(sum(amount),2) as total_amount,
round(sum(amount) * 100 / (select sum(amount) from payments ),2) as amount_pct
from payments 
where status = "failed" or "refunded"
group by method; 
 

-- ---------------------------------------------------(3).	Do riders who pay by wallet take more trips on average than those who pay by cash?

SELECT
    p.method,
    COUNT(t.trip_id)                                        AS total_trips,
    COUNT(DISTINCT t.rider_id)                              AS unique_riders,
    ROUND(COUNT(t.trip_id) * 1.0 / COUNT(DISTINCT t.rider_id), 2) AS avg_trips_per_rider
FROM payments AS p
JOIN trips AS t ON p.trip_id = t.trip_id
WHERE t.status = 'completed'
GROUP BY p.method
ORDER BY avg_trips_per_rider DESC;


-- -----------------------------------------------------------(4).	What is the average time between trip completion and payment (completed_at to paid_at)?
select 
round(avg(timestampdiff(hour,started_at, completed_at)),2) as "average trip duration (hour)",
round(avg(timestampdiff(minute, t.completed_at, p.paid_at)),2) as "avg_time_between_payment&_trip_completion (minutes)",
round(avg(timestampdiff(hour, t.completed_at, p.paid_at)),2) as "avg_time_between_payment&_trip_completion (hour)"
from trips as t
join payments as p
on t.trip_id = p.trip_id
where t.status = "completed" and p.status = "success"



