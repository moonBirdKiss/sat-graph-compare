from satellite import Satellite
from config import logger
import model
import skyfield.api
import config
import plot


class Constellation:
    def __init__(self, satellites, ground_stations):
        # ground_station is a list of (lat, lon), such as
        # ground_station = [[-120.55, 45.32], [], []]
        self.size = len(satellites)
        self.sats = satellites
        self.stations = ground_stations
        self.ground_num = len(ground_stations)

    # this method will return a matrix which reflect the connectivity of
    # certain timestamp, and timestamp is utc object
    def sat_graph(self, timestamp):
        # 这个函数返回的当前的卫星的物理通讯状态
        # 1. 如果两个卫星之间可以通讯，返回两个卫星之间的距离
        # 2. 如果不能通行就返回 -1
        # 3. 自己到自己的距离是 0
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
        # 这个方法用来构图
        # 1. 如果两个节点可以通信，就是1
        # 2. 如果两个节点不能通行就是0
        # 3. 自己到自己定为0
        res = self.sat_graph(timestamp)
        for i in range(len(res)):
            for j in range(len(res[i])):
                if res[i][j] > 0:
                    res[i][j] = 1
                else:
                    res[i][j] = 0
        return res

    def gs_connectivity(self, timestamp):
        # this method return the connectivity matrix of ground and sats
        sat_conn = self.sat_connectivity(timestamp)
        sum_num = self.size + self.ground_num
        gs_conn = [[0 for _ in range(sum_num)] for _ in range(sum_num)]

        for i in range(sum_num):
            for j in range(sum_num):
                if i < self.size and j < self.size:
                    gs_conn[i][j] = sat_conn[i][j]
                elif i >= self.size and j >= self.size:
                    if i == j:
                        gs_conn[i][j] = 0
                    else:
                        # ground station can communicate
                        gs_conn[i][j] = 1
                elif i >= self.size and j < self.size:
                    flag = self.sats[j].observe_sat(
                        self.stations[i - self.size][0], self.stations[i - self.size][1], timestamp)
                    if flag:
                        logger.debug(
                            f"Ground station {i - self.size} can observe satellite {j}")
                    gs_conn[i][j] = 1 if flag else 0
                else:
                    flag = self.sats[i].observe_sat(
                        self.stations[j - self.size][0], self.stations[j - self.size][1], timestamp)
                    if flag:
                        logger.debug(
                            f"Ground station {j - self.size} can observe satellite {i}")
                    gs_conn[i][j] = 1 if flag else 0
        return gs_conn

    def gs_connection(self, timestamp):
        sat_conn = self.sat_connection(timestamp)
        gs_conn = self.gs_connectivity(timestamp)
        sum_num = self.size + self.ground_num
        connection = [[(False, -1, -1) for _ in range(sum_num)]
                      for _ in range(sum_num)]
        for i in range(sum_num):
            for j in range(sum_num):
                if i < self.size and j < self.size:
                    connection[i][j] = sat_conn[i][j]
                elif i >= self.size and j >= self.size:
                    if i == j:
                        connection[i][j] = (False, -1, -1)
                    # ground station can communicate
                    else:
                        connection[i][j] = (
                            True, config.Ground_bandwidth, config.Ground_latency)
                else:
                    if gs_conn[i][j] == 1:
                        connection[i][j] = (
                            True, config.Ground_Sat_bandwidth, config.Ground_Sat_latency)
                    else:
                        connection[i][j] = (False, -1, -1)
        return connection

    def sat_connection(self, timestamp):
        # this method return [ [(flag, bandwidth, latency), (), ()],
        #                      [(), (), ()],
        #                      [(), (), ()] ]
        connectivity = self.sat_graph(timestamp)
        connection = [[(False, -1, -1) for _ in range(self.size)]
                      for _ in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if connectivity[i][j] > 0:
                    connection[i][j] = (True, model.from_dis_to_cbps(
                        connectivity[i][j] * 1000),  model.from_dis_to_latency(connectivity[i][j] * 1000))
                else:
                    connection[i][j] = (False, -1, -1)
        return connection

    def get_sats(self):
        return self.sats
    
    def get_station(self):
        return self.stations


# new_sats() create a constellation, default size is config.Constellation_scale
def new_sats(size=config.Constellation_scale, ground_num=config.Ground_num):
    stations_url = config.sat_TLE_path
    satellites = skyfield.api.load.tle_file(stations_url)
    by_number = {
        sat.model.satnum: sat for sat in satellites[:size]
    }
    logger.debug(by_number)
    sats = []
    for k, v in by_number.items():
        sats.append(Satellite(k, v))

    ground = []
    for i in range(ground_num):
        ground.append([config.Ground_locations[i][1][0],
                      config.Ground_locations[i][1][1]])
    c = Constellation(sats, ground)
    return c


if __name__ == "__main__":
    c = new_sats(5)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)

    graph = c.sat_graph(dt)
    logger.info(f"graph :{graph}")
    connectivity = c.sat_connectivity(dt)
    logger.info(f"connectivity: {connectivity}")
    connection = c.sat_connection(dt)
    logger.info(connection)


if __name__ == "__main__01":
    size = 3
    connection = [[(False, -1, -1) for _ in range(size)] for _ in range(size)]
    connection[0][1] = (True, 100, 100)
    connection[2][1] = (True, 200, 200)
    logger.info(connection)
