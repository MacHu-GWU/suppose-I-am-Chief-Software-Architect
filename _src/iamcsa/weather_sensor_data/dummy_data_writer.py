# -*- coding: utf-8 -*-

import rolex
import pandas as pd
from s3iotools.io.dataframe import S3Dataframe
from iamcsa.weather_sensor_data.device_id import rand_n_device
from iamcsa.weather_sensor_data.obs_type import obs_type_id_list

device_list = rand_n_device(n=1000)
hour_partition_key_list = rolex.time_series(
    "2018-01-01", "2018-01-31 23:59:59", freq="1H"
)

prefix = "/weather_sensor_data/lake"
for start_time in hour_partition_key_list:
    time_series = rolex.time_series(
        start_time, rolex.add_seconds(rolex.add_days(start_time, 1), -1), freq="5min"
    )
    for obs_type_id in obs_type_id_list:
        for device in device_list:
            device_id = device["device_id"]
            key = f"{prefix}/create_hour={start_time.date()}"
            break
        break
    break
    # for time in rolex.time_series():
