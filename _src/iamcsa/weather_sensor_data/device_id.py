# -*- coding: utf-8 -*-

import random
import uuid

lat_lower = 33.591582
lat_upper = 41.636246
lat_gap = lat_upper - lat_lower
lng_lower = -117.549870
lng_upper = -76.990342
lng_gap = lng_upper - lng_lower


def rand_lat_lng():
    lat = random.random() * lat_gap + lat_lower
    lng = random.random() * lng_gap + lng_lower
    return lat, lng


def rand_device_id():
    return str(uuid.uuid4())


def rand_n_device(n):
    device_list = list()
    for _ in range(n):
        device_id = rand_lat_lng()
        lat, lng = rand_lat_lng()
        device = {"device_id": device_id, "lat": lat, "lng": lng}
        device_list.append(device)
    return device_list
