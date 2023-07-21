from loguru import logger
import sys

# init logger
logger.remove()
# logger.add(
#     'out.log',
#     level='INFO'
# )

logger.add(
    sys.stdout,
    level='INFO'
)

# init constant
# Limit communication distance of laser communication: 65,000 km
LCTRange_m = 65 * 100 * 1000
radius_of_equator_m = 6378140  # 6356755m
radius_of_polar_m = 6356755  # 6356755m
Constellation_scale = 20  # size of constellation
radius_of_earth_m = 6371 * 1000  # radius of earth: m
height_of_atmosphere_m = 50 * 1000  # height of atmosphere: m


# config the graph similarity
iteration_time = 120 # 20 time
time_scale = 60 # 1min per time

sat_TLE_path = "/home/yqwang/Documents/sat-graph-compare/station.txt"
