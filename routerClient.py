import requests
import networkx as nx
from config import logger
from graphSimilarity import is_connected

url = 'http://127.0.0.1:8000/sat-route-update'


payload = {
    "sat_size": 50,
    "ground_size": 1,
    "index": 0
}
response = requests.post(url, json=payload)