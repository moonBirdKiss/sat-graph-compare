import requests
import networkx as nx
from config import logger
from graphSimilarity import is_connected

url = 'http://127.0.0.1:8000/gs-connectivity'


for i in range(60 * 60 * 24):
    payload = {
        "size": 50,
        "time": i * 60
    }
    logger.info(f"Time {i} Send Request")
    response = requests.post(url, json=payload)
    if is_connected(response.json()):
        logger.info(f"Time {i} is connected")