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
    def sat_graph(self, timestamp):
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

    def sat_connectivity(self, timestamp):
        res = self.sat_graph(timestamp)
        for i in range(len(res)):
            for j in range(len(res[i])):
                if res[i][j] > 0:
                    res[i][j] = 1
                else:
                    res[i][j] = 0
        return res
    
    def get_sats(self):
        return self.sats


# new_sats() create a constellation, default size is config.Constellation_scale
def new_sats(size=config.Constellation_scale):
    stations_url = config.sat_TLE_path
    satellites = skyfield.api.load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:size]
    }
    logger.debug(by_number)
    sats = []
    for k, v in by_number.items():
        sats.append(Satellite(k, v))
    c = Constellation(sats)
    return c


if __name__ == "__main__":
    c = new_sats()
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)

    graph = c.sat_graph(dt)
    logger.info(graph)
    plot.visulizeGraph(graph)
