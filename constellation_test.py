from constellation import *
import skyfield.api
from config import logger

def test_sat_connectivity():
    # 这个函数证明了python中的constellation类进行连接性计算是没有问题的
    cons = new_sats(3, 0)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 27, 23, 59, 7)
    res = cons.sat_graph(dt)
    sats = cons.get_sats()
    sats[0].info(dt)
    sats[1].info(dt)
    logger.info(res)

def test_sat_connection():
    # 这个函数证明了python中的constellation类进行连接性计算是没有问题的
    cons = new_sats(3, 0)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 27, 23, 59, 7)
    res1 = cons.sat_connectivity(dt)
    res2 = cons.sat_connection(dt)
    logger.info(f"res1: {res1}")
    logger.info(f"res2: {res2}")


def test_observe():
    # 这个函数证明了python中的constellation类进行地面观测性计算是没有问题的
    cons = new_sats(3, 1)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 27, 23, 59, 7)

    sats = cons.get_sats()
    sats[0].info(dt)
    sats[1].info(dt)
    sats[2].info(dt)

    grounds = cons.get_station()
    logger.info(f"grounds: {grounds[0]}")

    res = sats[0].observe_sat(grounds[0][0], grounds[0][1], dt)
    logger.info(f"sat0-res: {res}")

    res2 = sats[1].observe_sat(grounds[0][0], grounds[0][1], dt)
    logger.info(f"sat1-res2: {res2}")
    res1 = cons.gs_connectivity(dt)
    res2 = cons.gs_connection(dt)
    logger.info(f"res1: {res1}")
    logger.info(f"res2: {res2}")


if __name__ == "__main__":
    test_observe()