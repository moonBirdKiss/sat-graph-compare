import requests
import networkx as nx
from config import logger
from graphSimilarity import is_connected
import json
import plot


def test_sat_router():
    url = 'http://127.0.0.1:8000/sat-route-update'


    payload = {
        "sat_size": 50,
        "ground_size": 1,
        "index": 0
    }
    response = requests.post(url, json=payload)


def test_gs_connectivity():
    # Define the URL and the payload
    url = 'http://127.0.0.1:8000/gs-connectivity'
    for i in range(48, 100):
        payload = {'size': 49, 'time': 10 * i}

        logger.info(f"this is the index: {i}")

        # Send the POST request
        response = requests.post(url, data=json.dumps(payload), headers={'Content-Type': 'application/json'})

        # If the request was successful (HTTP status code 200), print the adjacency matrix
        if response.status_code == 200:
            adjacency_matrix = response.json()
            print(adjacency_matrix)
        else:
            print('Request failed with status code', response.status_code)
        
        plot.visulizeGraph(adjacency_matrix)



if __name__ == "__main__":
    test_gs_connectivity()