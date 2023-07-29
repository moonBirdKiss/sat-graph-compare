import requests
import networkx as nx
from config import logger
from graphSimilarity import is_connected
import json
import plot


def test_sat_router():
    url = 'http://127.0.0.1:8000/sat-route-update'

    payload = {
        "sat_size": 7,
        "ground_size": 1,
        "index": 0
    }
    response = requests.post(url, json=payload)


def test_sat_router():
    # Define the URL and the payload
    url = 'http://192.168.1.29:8000/sat-route-update'
    for i in range(0, 1):
        payload = {
            'sat_size': 7, 
            'time': 60 * i,
            'ground_size': 1,
            'index': 5
        }

        logger.info(f"this is the index: {60 * i}")

        # Send the POST request
        response = requests.post(url, data=json.dumps(payload), headers={
                                 'Content-Type': 'application/json'})

        adjacency_matrix = []
        # If the request was successful (HTTP status code 200), print the adjacency matrix
        if response.status_code == 200:
            adjacency_matrix = response.json()
            print(adjacency_matrix)
        else:
            print('Request failed with status code', response.status_code)

        # plot.visulizeGraph(adjacency_matrix)

def test_gs_connectivity():
    # Define the URL and the payload
    url = 'http://192.168.1.29:8000/gs-connectivity'
    for i in range(0, 40):
        payload = {
            'size': 8, 
            'time': 60 * i,
            'ground_size': 1,
            'index': 5
        }

        logger.info(f"this is the index: {60 * i}")

        # Send the POST request
        response = requests.post(url, data=json.dumps(payload), headers={
                                 'Content-Type': 'application/json'})

        adjacency_matrix = []
        # If the request was successful (HTTP status code 200), print the adjacency matrix
        if response.status_code == 200:
            adjacency_matrix = response.json()
            print(adjacency_matrix)
        else:
            print('Request failed with status code', response.status_code)

        plot.visulizeGraph(adjacency_matrix)


def test_bent_pipe():
    # Define the URL and the payload
    url = 'http://192.168.1.29:8000/bent-pipe'
    for i in range(0, 1):
        payload = {
            'sat_size': 8, 
            'time': 60 * i,
            'ground_size': 1,
            'index': 5
        }

        logger.info(f"this is the index: {60 * i}")

        # Send the POST request
        response = requests.post(url, data=json.dumps(payload), headers={
                                 'Content-Type': 'application/json'})

        adjacency_matrix = []
        # If the request was successful (HTTP status code 200), print the adjacency matrix
        if response.status_code == 200:
            adjacency_matrix = response.json()
            print(adjacency_matrix)
        else:
            print('Request failed with status code', response.status_code)

        # plot.visulizeGraph(adjacency_matrix)


if __name__ == "__main__":
    test_gs_connectivity()
