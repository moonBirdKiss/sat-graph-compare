from loguru import logger
import sys

# init logger
logger.remove()
# logger.add(
#     'out.log',
#     level='INFO'
# )

logger.add(sys.stdout, level='INFO')

# init constant
# Limit communication distance of laser communication: 65,000 km
LCTRange_m = 65 * 100 * 1000
radius_of_equator_m = 6378140  # 6356755m
radius_of_polar_m = 6356755  # 6356755m
Constellation_scale = 20  # size of constellation
radius_of_earth_m = 6371 * 1000  # radius of earth: m
height_of_atmosphere_m = 50 * 1000  # height of atmosphere: m
Link_angle = 15  # link angle: degree

# config the graph similarity
iteration_time = 10  # 20 time
time_scale = 60  # 1min per time

# config the ground station
Ground_locations = [["Test", [2.85, 57.13]],
                    ["US (Oregon)", [-120.5542, 45.3238]],
                    ["US (Ohio)", [-82.7649, 40.4173]],
                    ["Middle East (Bahrain)", [50.5354, 26.2212]],
                    ["Europe (Stockholm)", [18.0649, 59.3328]],
                    ["Asia Pacific (Sydney)", [151.2093, -33.8688]],
                    ["Europe (Ireland)", [-6.2675, 53.3441]],
                    ["Africa (Cape Town)", [18.4232, -33.9249]],
                    ["US (Hawaii)", [-157.8583, 21.3069]],
                    ["Asia Pacific (Seoul)", [126.9780, 37.5665]],
                    ["Asia Pacific (Singapore)", [103.8198, 1.3521]]]

Ground_bandwidth = 10 * 1000 * 1000 * 1000  # 10Gbps
Ground_latency = 40  # ms
Ground_Sat_bandwidth = 1 * 1000 * 1000 * 1000  # 1Gbps
Ground_Sat_latency = 20  # ms
Ground_num = 1

sat_TLE_path = "/home/dqf/Documents/python/sat-graph-compare/station.txt"
res_path = "/home/dqf/Documents/python/sat-graph-compare/res/"

# pi configuration
NodeList = [
    "edge-0", "edge-1", "edge-2", "edge-3", "edge-4", "edge-5", "edge-6",
    "master"
]
