Weather Data Sensor
==============================================================================

Business I do. I have a small, easy to install device, solar power battery backed device. Can receive GPS signal, and collection 10 different observations every 5 seconds.

We installed 20,000 devices all over the USA.

It generates:

- 20,000 * 10 * (60 / 5) = 2.4 M per minutes
- 144 M per hour
- 3.4 B per day

Device ->
Kinesis ->
Lambda
    -> DynamoDB
    -> Backup S3
    -> DataLake S3



Raw data
------------------------------------------------------------------------------

- device_id, uuid4
- observation_type_id, int
- time, string
- value,

in csv format, 70KB / 1000 rows, Kinesis stream take max 6MB payload.
we can do 50000 rows each invoke, and it is 3.5MB payload


Backup S3
------------------------------------------------------------------------------
/


DataLake S3
------------------------------------------------------------------------------

/<date>/<hour>/<observation_type>/<invokation-id>.parquet

txt schema:

- device_id
- time
- value

based on this partition strategy, 14.4 M rows per partition


Data Call Pattern
------------------------------------------------------------------------------


Find weather data in period of time for certain location
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    device_id = find_device_id_by_lat_lng(lat, lng)

    SELECT
        O.observation_type,
        O.time,
        O.value
    FROM observation O
    WHERE
        observation.date BETWEEN :start AND :end
        AND O.device_id = :device_id
    ORDER BY O.observation_type ASC, O.time ASC
