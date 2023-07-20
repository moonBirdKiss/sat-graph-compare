from satellite import Satellite
from config import logger
import copy
import skyfield.api
import config
import plot


class Constellation:
    def __init__(self, satellites):
        self.size = len(satellites)
        self.sats = satellites

    # this method will return a matrix which reflect the connectivity of
    # certain timestamp, and timestamp is utc object
    def satellite_graph(self, timestamp):
        res = []
        for i, sat in enumerate(self.sats):
            node_connectivity = []
            for j, sat2 in enumerate(self.sats):
                if sat != sat2:
                    flag, dis_km = sat.dis_to_another_sat(sat2, timestamp)

                    if flag:
                        node_connectivity.append(dis_km)
                    else:
                        node_connectivity.append(-1)
                else:
                    node_connectivity.append(0)
            res.append(node_connectivity)
        return res


if __name__ == "__main__":
    stations_url = "/Users/dengquanfeng/files/project/spaceGround/INFOCOM/image/python/LEO-tools/LEODistance/station.txt"
    satellites = skyfield.api.load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:config.Constellation_scale]
    }
    logger.debug(by_number)

    sats = []
    for k, v in by_number.items():
        sats.append(Satellite(k, v))

    c = Constellation(sats)

    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)

    graph = c.satellite_graph(dt)
    logger.info(graph)
    plot.visulizeGraph(graph)
