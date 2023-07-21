# this module is used to check the satellites are LEO satellite
import config
from config import logger
import constellation
from skyfield.api import load


def check_sats_LEO(sats):
    bad_sat = []
    ts = load.timescale()
    timestamp = ts.utc(2023, 7, 20, 12, 20, 29)
    for index, sat in enumerate(sats):
        _, _, height, number = sat.info(timestamp)
        if height > 1000:
            bad_sat.append(sat)
    
    return bad_sat
        


if __name__ == "__main__":

    cons = constellation.new_sats(292 // 3)
    sats = cons.get_sats()
    bad_sat = check_sats_LEO(sats)

    ts = load.timescale()
    timestamp = ts.utc(2023, 7, 20, 12, 20, 29)

    for sat in bad_sat:
        _, _, height, number = sat.info(timestamp)
        logger.info(f"number: {number}, height: {height}")