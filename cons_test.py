import constellation
import skyfield.api
from config import logger


if __name__ == "__main__":
    c = constellation.new_sats(3, 1)
    ts = skyfield.api.load.timescale()

    dt = ts.utc(2023, 7, 20, 12, 20, 30 + 100)
    res1 = c.sat_connection(dt)

    dt = ts.utc(2023, 7, 20, 12, 20 + 1, 30 + 41)   
    res2 = c.sat_connection(dt)

    logger.info(res1)
    logger.info(res2)
