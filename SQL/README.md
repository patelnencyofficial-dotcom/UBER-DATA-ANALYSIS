# SQL Analysis Index

This folder contains 40+ business questions answered directly in SQL — the analysis layer this project was built on *before* any Python or charting touched the data. Some of these were later explored further in `python/EDA_and_ML.py` and visualized; others (especially data validation and a few foundational KPIs) exist only here in SQL, and that's intentional — not every finding needs a chart to be valuable. A null-check or a foreign-key validation query, for example, is exactly as important to a real analytics workflow as a chart, it just isn't something you visualize.

**Legend:** ✅ = also charted in Python &nbsp;&nbsp;|&nbsp;&nbsp; — = SQL-only finding

---

## 01_data_validation_and_cleaning.sql
*Foundational data-quality work — nothing here gets a chart, but nothing downstream is trustworthy without it.*

- — Null-value checks across all 8 tables (`cancellations`, `users`, `riders`, `drivers`, `trips`, `payments`, `locations`, `reviews`)
- — Foreign-key integrity checks via `LEFT JOIN` (orphaned cancellations, drivers without users, payments without trips, reviews without trips, riders without users, trips without valid riders/drivers)

## 02_descriptive.sql
*Quick top-line health check — the numbers a stakeholder asks for first.*

- — Total completed trips
- — Completed vs. cancelled trip counts
- — Total revenue by payment method
- — Average fare per trip

## 03_core_business_analytics.sql
*Exploratory pass across trips, riders, drivers, and locations — broader and less structured than the other files, used to sanity-check patterns before formalizing them elsewhere.*

- — Total trips per day / per month / per year-month
- — Hourly trip counts
- — Monthly trip count + revenue together
- — Total trips per rider; active riders (50+ trips)
- — Old vs. new riders (by join year)
- — Total spend per rider; top 10 riders by spend
- — High-value vs. low-value rider segmentation ($1,500 threshold)
- — Trips + earnings per driver
- — Active vs. inactive driver flag; count of each
- — Average rating per driver; high-rated (>4.5) vs. low-rated (<3) drivers
- ✅ Most popular pickup zones by trip count (see `19_top_pickup_zones_revenue.png`)

## 04_trip_performance_and_volume.sql
*Operational metrics — how big is the platform, and when is it busiest?*

1. — Total trips, and % completed vs. cancelled vs. other statuses
2. — Avg / min / max / stddev of trip distance (km)
3. — Avg / min / max trip duration (minutes)
4. — Avg wait time (`requested_at` → `started_at`)
5. — Trips per hour of day; top 3 peak hours
6. — Trip volume by day of week
7. ✅ Monthly trip volume trend, MoM change (`01_monthly_revenue_trend.png`)
8. ✅ % of trips using surge pricing, avg surge level (`02_surge_tier_avg_fare.png`, `03_surge_tier_boxplot.png`)

## 05_revenue_performance.sql
*The financial core of the analysis.*

1. — Total revenue, avg fare per trip, revenue per km
2. ✅ Revenue & avg fare trend, month over month (`01_monthly_revenue_trend.png`)
3. ✅ Avg fare & trip count by surge tier: No / Low / High (`02_surge_tier_avg_fare.png`)
4. ✅ Fare distribution across 5 buckets (`04_fare_bucket_distribution.png`, `05_fare_histogram.png`)
5. ✅ Revenue vs. avg fare by hour of day (`06_revenue_by_hour.png`)
6. — What % of revenue comes from the top 10% of trips by fare? (Pareto analysis via `NTILE`)
7. — Revenue lost from cancelled trips (using `base_fare`)

## 06_driver_analysis.sql
*Who's driving the platform, literally and financially.*

1. ✅ Top 10 drivers by total trips and earnings (`07_top10_drivers_earnings.png`)
2. ✅ Driver rating distribution, 0.5-point buckets (`08_driver_rating_distribution.png`)
3. ✅ Do higher-rated drivers earn more per trip? (`09_avg_fare_by_driver_rating.png`)
4. ✅ % of drivers active vs. inactive (`10_active_vs_inactive_drivers.png`)
5. ✅ Most common vehicle make/model; effect on fare & distance (`11_vehicle_make_analysis.png`)
6. ✅ Avg trips per driver per month, min–max range (`12_trips_per_driver_per_month.png`)
7. ✅ Driver tenure vs. rating — does experience correlate with rating? (`13_driver_tenure_vs_rating.png`)

## 07_rider_behaviour_and_retention.sql
*Who rides, how often, and how long they stick around.*

1. ✅ Top 10 riders by lifetime spend and total trips (`14_top10_riders_spend.png`)
2. ✅ Rider segmentation — Low (1–5) / Medium (6–20) / High (20+) trips — and revenue share (`15_revenue_by_rider_segment.png`)
3. ✅ Rider rating distribution; % of riders below 4.0 (`16_rider_rating_distribution.png`)
4. ✅ New rider acquisition trend by month (`17_new_rider_acquisition.png`)
5. — Avg time gap between a rider's 1st and 2nd trip (early retention signal)
6. ✅ Which cities have the highest avg rider spend per trip? (`18_avg_fare_by_city.png`)

## 08_location_and_zone_analysis.sql
*Where the business actually happens.*

1. ✅ Top pickup zones by trip count and revenue (`19_top_pickup_zones_revenue.png`)
2. ✅ Avg fare by zone type — commercial vs. residential vs. airport (`20_avg_fare_by_zone_type.png`)
3. ✅ Top 10 pickup → dropoff corridors (`21_top_corridors.png`)
4. ✅ Dropoff zones with the longest avg trip distance (`22_dropoff_zones_avg_distance.png`)
5. ✅ Zones with the highest cancellation rate (`23_zone_cancellation_rate.png`)

## 09_cancellation_deep_dive.sql
*Why trips fail to happen.*

1. ✅ Overall cancellation rate; driver vs. rider split (`24_cancellation_driver_vs_rider.png`)
2. ✅ Top 5 cancellation reasons, separately for drivers and riders (`25_cancellation_reasons.png`)
3. ✅ Do lower-rated drivers cancel more? By rating bucket (`26_cancel_rate_by_driver_rating.png`)
4. ✅ Cancellations by hour of day (`27_cancellations_by_hour.png`)
5. — Riders who've cancelled more than 3 trips (repeat cancellers, flagged for ops follow-up)

## 10_payments_and_financial_ops.sql
*The money-movement layer.*

1. ✅ Split of payment methods — wallet / card / cash — by count and amount (`28_payment_method_split.png`)
2. ✅ Payment failure rate per method (`29_payment_failure_rate.png`)
3. ✅ Do wallet users take more trips on average than cash users? (`30_avg_trips_by_payment_method.png`)
4. ✅ Avg time between trip completion and payment (`31_payment_settlement_time.png`)

## 11_revenue_and_satisfaction.sql
*Does money buy happiness — do riders and drivers rate each other fairly?*

1. ✅ Avg review rating — riders → drivers vs. drivers → riders (`32_avg_ratings_both_directions.png`)
2. ✅ Lowest-rated drivers with 5+ reviews (`33_bottom10_drivers_review.png`)
3. ✅ Relationship between trip fare and review rating (`34_rating_by_fare_bucket.png`)
4. ✅ % of completed trips that get a review — submission rate (`35_review_submission_rate.png`)

---

## Coverage summary

| File | Questions | Charted | SQL-only |
|---|---|---|---|
| 01_data_validation_and_cleaning.sql | 2 checks | 0 | 2 |
| 02_descriptive.sql | 4 | 0 | 4 |
| 03_core_business_analytics.sql | 11 | 1 | 10 |
| 04_trip_performance_and_volume.sql | 8 | 2 | 6 |
| 05_revenue_performance.sql | 7 | 4 | 3 |
| 06_driver_analysis.sql | 7 | 7 | 0 |
| 07_rider_behaviour_and_retention.sql | 6 | 5 | 1 |
| 08_location_and_zone_analysis.sql | 5 | 5 | 0 |
| 09_cancellation_deep_dive.sql | 5 | 4 | 1 |
| 10_payments_and_financial_ops.sql | 4 | 4 | 0 |
| 11_revenue_and_satisfaction.sql | 4 | 4 | 0 |
| **Total** | **~60** | **36** | **~24** |

Roughly 40% of the SQL questions were answered in SQL only and never made it into a chart — mostly data validation, exploratory groundwork, and a few operational deep-dives (repeat cancellers, revenue lost to cancellations, the Pareto/top-10% revenue analysis) that are more useful as a number in a report than as a visual.
