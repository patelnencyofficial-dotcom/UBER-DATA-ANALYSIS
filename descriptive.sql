#--------------descriptive analysis (hos the company doing )-----------

#--------total trips -------------
select count(*) as total_trips
from trips 
where status = "completed"
;

#-----------completed vs cancelled trips -----------

select status, count(status) as trips
from trips
group by status;

#----------total revenue -----------------
select method ,round(sum(amount) )as total_revenue 
from payments
where status= "success"
group by method ;

#------------average fair per trip ---------
select round(avg(amount),2) as average_cost_per_trip
from payments
where status = "success";

