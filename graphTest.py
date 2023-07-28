from graphSimilarity import *
from  config import logger
import constellation
import skyfield.api
import networkx as nx   

def test_change_compare():
    matrix1 = [
        [0, 1, 1, 0],
        [1, 0, 1, 0],
        [1, 1, 0, 1],
        [0, 0, 1, 0]
    ]
    matrix2 = [
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 1, 0]
    ]
    # plot.visulizeGraph(matrix1)
    # plot.visulizeGraph(matrix2)
    change_count = compare_adjacency_matrices(matrix1, matrix2)
    print("Number of changes:", change_count)


def test_sat_compare():
    cons = constellation.new_sats(50,0)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)
    g1 = cons.sat_connectivity(dt)
    res = []
    for i in range(60):
        dt = ts.utc(2023, 7, 20, 12, 20 + i , 29)
        g2 = cons.sat_connectivity(dt)
        change_count = compare_adjacency_matrices(g1, g2)
        g1 = g2
        logger.info(f"Number of changes: {change_count}")
        res.append(change_count)
    return res

def test_gs_compare():
    cons = constellation.new_sats(50,10)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)
    g1 = cons.gs_connectivity(dt)
    res = []
    for i in range(60):
        dt = ts.utc(2023, 7, 20, 12, 20 + i, 29)
        g2 = cons.gs_connectivity(dt)
        change_count = compare_adjacency_matrices(g1, g2)
        g1 = g2
        logger.info(f"Number of changes: {change_count}")
        res.append(change_count)
    return res



def test_common_sub():
    matrix1 = [[0, 1, 1, 0], 
               [1, 0, 1, 0], 
               [1, 1, 0, 1], 
               [0, 0, 1, 0]]
    
    matrix2 = [[0, 1, 0, 0], 
               [1, 0, 0, 0], 
               [0, 0, 0, 1], 
               [0, 0, 1, 0]]
    
    matrix3 = [[0, 0, 1, 0], 
               [0, 0, 1, 0], 
               [1, 1, 0, 1], 
               [0, 0, 1, 0]]

    common_matrix = common_subgraph([matrix1, matrix2])
    print("Common subgraph adjacency matrix:", common_matrix)


def test_get_same_link(time_scale=10, start_time=0):
    cons = constellation.new_sats(50,10)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20 + start_time, 29)
    res = []

    # set the init graph
    g1 = cons.gs_connectivity(dt)

    for i in range(1, time_scale):
        dt = ts.utc(2023, 7, 20, 12, 20 + start_time + i , 29)
        g2 = cons.gs_connectivity(dt)
        res.append(g1)
        common_matrix = common_subgraph([g1, g2])
        size = np.count_nonzero(common_matrix)
        flag = is_connected(common_matrix)
        logger.info(f"{i}: Common subgraph adjacency matrix: {size}, flag: {flag}")
        res.append(res)
        g1 = common_matrix
    return size

def get_gs_same_link(file_name,time_scale=30, start_time=0, satnum=50):
    cons = constellation.new_sats(satnum,10)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20 + start_time, 29)

    # set the init graph
    g1 = cons.gs_connectivity(dt)
    
    FILE = open(file_name, "w")
    
    for i in range(1, time_scale+1):
        dt = ts.utc(2023, 7, 20, 12, 20 + start_time + i , 29)
        g2 = cons.gs_connectivity(dt)
        common_matrix = common_subgraph([g1, g2])
        size = np.count_nonzero(common_matrix)
        flag = is_connected(common_matrix)
        logger.info(f"{i}: Common subgraph adjacency matrix: {size}, flag: {flag}")
        FILE.write("deltaT: "+str(i)+"############\n")
        FILE.write(str(size)+"\n")
        g1 = common_matrix
    FILE.close()

def get_sat_same_link(file_name,time_scale=30, start_time=0, satnum=50):
    cons = constellation.new_sats(satnum,10)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20 + start_time, 29)

    # set the init graph
    g1 = cons.sat_connectivity(dt)
    
    FILE = open(file_name, "w")
    
    for i in range(1, time_scale+1):
        dt = ts.utc(2023, 7, 20, 12, 20 + start_time + i , 29)
        g2 = cons.sat_connectivity(dt)
        common_matrix = common_subgraph([g1, g2])
        size = np.count_nonzero(common_matrix)
        flag = is_connected(common_matrix)
        logger.info(f"{i}: Common subgraph adjacency matrix: {size}, flag: {flag}")
        FILE.write("deltaT: "+str(i)+"############\n")
        FILE.write(str(size)+"\n")
        g1 = common_matrix
    FILE.close()

def test_is_connect():
    matrix3 = [[0, 0, 1, 0], 
            [0, 0, 1, 0], 
            [1, 1, 0, 1], 
            [0, 0, 1, 0]]
        
    matrix2 = [[0, 1, 0, 0], 
               [1, 0, 0, 0], 
               [0, 0, 0, 1], 
               [0, 0, 1, 0]]
    print(is_connected(matrix2), is_connected(matrix3))
    

if __name__ == "__main__":
    
    for start_time in range(60,120):
        file_name = "./gs_record/sec"+str(start_time)+".txt"
        get_gs_same_link(file_name,start_time=start_time)