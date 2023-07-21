from skyfield.api import load, wgs84, utc
from datetime import datetime
from math import *
import math
from loguru import logger

import config
from config import logger


class Point:
    # The Point class is a latitude and longitude coordinate
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    # Calculate the distance between two points in meters
    def cal_distance_to_point(self, point):
        if self.lat == point.lat and self.lon == point.lon:
            return 0

        latA = self.lat
        lonA = self.lon
        latB = point.lat
        lonB = point.lon

        ra = config.radius_of_equator_m              # radius of equator: meter
        rb = config.radius_of_polar_m              # radius of polar: meter
        flatten = (ra - rb) / ra  # Partial rate of the earth
        # change angle to radians
        radLatA = radians(latA)
        radLonA = radians(lonA)
        radLatB = radians(latB)
        radLonB = radians(lonB)
        pA = atan(rb / ra * tan(radLatA))
        pB = atan(rb / ra * tan(radLatB))
        x = acos(sin(pA) * sin(pB) + cos(pA) *
                 cos(pB) * cos(radLonA - radLonB))
        c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2
        c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2
        dr = flatten / 8 * (c1 - c2)
        distance = ra * (x + dr)
        return distance


# for simulating the movement of satellites
class Satellite:
    def __init__(self, number, satnum):
        self.number = number
        self.satellite = satnum
        self.lat = 0
        self.lon = 0
        self.height = 0  # km

    # print the infomation of the satellite at a certain time
    def info(self, timestamp):
        self.update_pos(timestamp)
        logger.debug(
            f"Satellite number: {self.number}, self.lat: {self.lat}, self.lon: {self.lon}, self.height: {self.height}"
        )
        return self.lat, self.lon, self.height, self.number

    # timestamp is a utc object
    # ts = load.timescale()
    # timestamp = ts.utc(2023, 7, 20, 12, 20, 29)

    def point_project_at_ground(self, timestamp):
        geocentric = self.satellite.at(timestamp)
        sp = wgs84.subpoint(geocentric)
        height = wgs84.height_of(geocentric).km
        logger.debug(f'Latitude: {sp.latitude.degrees}')
        logger.debug(f'Longitude: {sp.longitude.degrees}')
        logger.debug(f'height: {height}')
        return sp.latitude.degrees, sp.longitude.degrees, height

    # Return the distance from the satellite position at a certain time (ground projection point)
    # to the specified latitude and longitude coordinates
    def get_distance(self, timestamp, point):
        lat, log, _ = self.NE_subpoint_at_time(timestamp)
        my_point = Point(lat, log)
        distance = my_point.cal_distance_to_point(point)
        return distance

    # Return the angle and distance between the satellite's position at a certain time and a certain point on the ground

    def get_relative_point_to_ground_point(self, timestamp, point):
        ts = load.timescale()
        date = datetime.fromtimestamp(int(timestamp))
        date = date.replace(tzinfo=utc)
        t = ts.from_datetime(date)

        lat = point.lat
        lon = point.lon
        bluffton = wgs84.latlon(lat, lon)
        difference = self.satellite - bluffton
        topocentric = difference.at(t)
        alt, az, distance = topocentric.altaz()

        return alt.degrees, az.degrees, distance.km

    # update position
    def update_pos(self, timestamp):
        lat, lon, height = self.point_project_at_ground(timestamp)
        self.lat = lat
        self.lon = lon
        self.height = height

    # Obtain the straight-line distance to another satellite
    # and judge whether the two satellites can communicate directly
    # and the return is in km
    def dis_to_another_sat(self, anotherSat, timestamp):
        self.update_pos(timestamp)
        anotherSat.update_pos(timestamp)

        p1 = Point(self.lat, self.lon)
        p2 = Point(anotherSat.lat, anotherSat.lon)

        p1_h = self.height
        p2_h = anotherSat.height

        p1_h += config.radius_of_earth_m / 1000
        p2_h += config.radius_of_earth_m / 1000

        # Get the ground distance (meters) between two points
        p2pdist_ground = p1.cal_distance_to_point(p2)

        # The angle between two points relative to the center of the earth
        # the radius of the earth is 6371000
        rad = p2pdist_ground / config.radius_of_earth_m
        if rad > math.pi:
            rad = 2 * math.pi - rad

        # Find the distance between two satellites by the law of cosines
        if (math.pow(p1_h, 2) + math.pow(p2_h, 2) - 2 * p1_h * p2_h * math.cos(rad)) < 0:
            return 0, 0
        dis_km = math.sqrt(math.pow(p1_h, 2) + math.pow(p2_h, 2) -
                           2 * p1_h * p2_h * math.cos(rad))

        # Find the heigh from the center of the earth to the line connecting two satellites
        # If the heigh >= r + r_of_atmosphere, the two satellites can communicate directly, else not
        ifreachable = True

        height_of_line_km = (p1_h * p2_h * math.sin(rad)) / dis_km
        if dis_km > config.LCTRange_m / 1000:
            logger.debug(
                f"{self.number} and {anotherSat.number}: The distance is too far to communicate directly"
            )
            ifreachable = False

        if height_of_line_km < config.radius_of_earth_m / 1000 + config.height_of_atmosphere_m / 1000:
            logger.debug(
                f"{self.number} and {anotherSat.number}: The atomsphere is too thick to communicate directly"
            )
            ifreachable = False

        return ifreachable, dis_km


if __name__ == "__main__":
    stations_url = "./station.txt"
    satellites = load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:config.Constellation_scale]
    }
    logger.debug(by_number)
    s0 = Satellite(44734, by_number[44734])
    s1 = Satellite(44721, by_number[44721])
    s2 = Satellite(44749, by_number[44740])
    s3 = Satellite(44744, by_number[44744])

    # 指定的日期
    # dt = datetime(2023, 7, 20, 20, 20, 29).timestamp()
    ts = load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)
    s0.info(dt)
    s1.info(dt)
    s2.info(dt)
    s3.info(dt)
    logger.info(s0.dis_to_another_sat(s1, dt))
    logger.info(s0.dis_to_another_sat(s2, dt))
    logger.info(s0.dis_to_another_sat(s3, dt))
