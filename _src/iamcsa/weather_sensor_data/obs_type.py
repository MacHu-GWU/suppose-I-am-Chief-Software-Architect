# -*- coding: utf-8 -*-

from constant2 import Constant


class ObsType(Constant):
    class Temperature(Constant):
        id = 1
        name = "temperature"

    class Humidity(Constant):
        id = 2
        name = "humidity"

    class WindSpeed(Constant):
        id = 3
        name = "windspeed"

    class SolarPower(Constant):
        id = 4
        name = "solarpower"


obs_type_id_list = ObsType.SubIds(id_field="id", sort_by="id")

if __name__ == "__main__":
    print(obs_type_id_list)
