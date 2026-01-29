-- Question 1 - What's the version of pip in the image?
docker run -it --entrypoint=bash python:3.13
pip -V
-- Answer: 25.3

-- Question 2 - Given the following docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?

--Answer:
postgres:5432
db:5432

postgres is a container name and db is a service name, so both answers are correct

-- Question 3 - For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

SELECT COUNT(*) AS count_trips FROM public.yellow_taxi_trips
WHERE lpep_pickup_datetime between '2025-11-01' and '2025-12-01'
AND trip_distance <= 1

-- Answer: 8007

-- Question 4 - Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

SELECT DATE(lpep_pickup_datetime) AS Day FROM public.yellow_taxi_trips
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1

-- Answer: 2025-11-14

--Question 5 - Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

SELECT tz."Zone" as pickup_zone, COUNT(*) count_trips FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tz
	ON tz."LocationID" = tt."PULocationID"
WHERE DATE(lpep_pickup_datetime) = '2025-11-18' 
GROUP BY tz."Zone"
ORDER BY COUNT(*) DESC
LIMIT 1

-- Answer: East Harlem North

-- Question 6 - For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

SELECT 
    tzd."Zone" AS dropoff_zone, 
    tt.tip_amount AS sum_tip
FROM public.yellow_taxi_trips tt
JOIN public.taxi_zones tzp
    ON tzp."LocationID" = tt."PULocationID"
JOIN public.taxi_zones tzd
    ON tzd."LocationID" = tt."DOLocationID"
WHERE EXTRACT(MONTH FROM tt.lpep_pickup_datetime) = 11
  AND EXTRACT(YEAR FROM tt.lpep_pickup_datetime) = 2025
  AND tzp."Zone" = 'East Harlem North'
ORDER BY sum_tip DESC
LIMIT 1;

-- Answer: Yorkville West

-- Question 7 - Which of the following sequences, respectively, describes the workflow for:
-- 1. Downloading the provider plugins and setting up backend,
-- 2. Generating proposed changes and auto-executing the plan
-- 3. Remove all resources managed by terraform`

-- Answer: terraform init, terraform apply -auto-approve, terraform destroy