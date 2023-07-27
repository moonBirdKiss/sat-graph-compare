from satellite import *
import skyfield.api


def test_sat_position():
    # 此时证明了python中的satellite类进行定位是没有问题的
    stations_url = "./station.txt"
    satellites = load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:config.Constellation_scale]
    }
    logger.debug(by_number)
    s0 = Satellite(49774, by_number[49774])
    s1 = Satellite(49775, by_number[49775])
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 27, 23, 59, 27)
    s0.info(dt)
    s1.info(dt)


def test_sat_distance():
    # 此时基本可以判断 python中的satellite类进行距离计算是没有问题的
    stations_url = "./station.txt"
    satellites = load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:config.Constellation_scale]
    }
    logger.debug(by_number)

    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 27, 13, 4, 50)

    s0 = Satellite(39439, by_number[39439])
    s1 = Satellite(43780, by_number[43780])
    s2 = Satellite(44398, by_number[44398])
    flag, dis_km = s0.dis_to_another_sat(s1, dt)
    logger.info(f"flag:{flag}, dis_km: {dis_km}")
    flag, dis_km = s0.dis_to_another_sat(s2, dt)
    logger.info(f"flag:{flag}, dis_km: {dis_km}")



if __name__ == "__main__":
    test_sat_distance()