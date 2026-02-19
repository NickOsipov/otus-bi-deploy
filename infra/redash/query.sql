SELECT COUNT(*) as cnt, payment_type
FROM default.trips
GROUP BY payment_type

SELECT COUNT(trip_id) as cnt, HOUR(pickup_datetime) AS hour
FROM default.trips
GROUP BY hour
ORDER BY hour