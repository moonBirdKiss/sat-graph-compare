from satellite import Satellite
from config import logger
import model
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
    
    def sat_connection(self, timestamp):
        # this method return [ [(flag, bandwidth, latency), (), ()], 
        #                      [(), (), ()],
        #                      [(), (), ()] ]
        connectivity = self.sat_graph(timestamp)
        connection = [ [ (False, -1, -1) for _ in range(self.size)] for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if connectivity[i][j] > 0:
                    connection[i][j] = (True, model.from_dis_to_cbps(connectivity[i][j] * 1000),  model.from_dis_to_latency(connectivity[i][j] * 1000))
                else:
                    connection[i][j] = (False, -1, -1)
        return connection
    
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
    c = new_sats(5)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)

    graph = c.sat_graph(dt)
    logger.info(graph)
    connectivity = c.sat_connectivity(dt)
    logger.info(connectivity)
    connection = c.sat_connection(dt)
    logger.info(connection)
    

if __name__ == "__main__01":
    size = 3
    connection = [ [ (False, -1, -1) for _ in range(size)] for _ in range(size)]
    connection[0][1] = (True, 100, 100)
    connection[2][1] = (True, 200, 200)
    logger.info(connection)