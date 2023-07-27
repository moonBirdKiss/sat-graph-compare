from config import logger
from astra_topology import *
import numpy as np
import plot


def test_sub_graph():
    # 测试函数
    adj_matrix = np.array([[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 0, 0],
                           [0, 0, 0, 0, 1], [0, 0, 0, 1, 0]])

    subgraph_adj_matrices = get_connected_subgraph_adj_matrices(adj_matrix)

    for i, subgraph_matrix in enumerate(subgraph_adj_matrices):
        print(f"Subgraph {i+1}:")
        print(subgraph_matrix)


def test_spanning_tree():
    adj_matrix = np.array([[0, 1, 0, 0, 0], [1, 0, 1, 0, 0], [0, 1, 0, 1, 1],
                           [0, 0, 1, 0, 1], [0, 0, 1, 1, 0]])
    plot.visulizeGraph(adj_matrix)

    mst_adj_matrix = get_minimum_spanning_tree(adj_matrix)
    print(mst_adj_matrix)
    plot.visulizeGraph(mst_adj_matrix.tolist())


def test_max_degree():
    # 测试函数
    adj_matrix = np.array([[0, 1, 0, 1, 0], [1, 0, 1, 1, 0], [0, 1, 0, 1, 1],
                           [1, 1, 1, 0, 1], [0, 0, 1, 1, 0]])
    plot.visulizeGraph(adj_matrix)
    max_degree_node = get_max_degree_node(adj_matrix)
    print(max_degree_node)


def test_generate_tree():
    G = generate_complete_graph(6)
    ret = generate_tree(G, 4)
    plot.visulizeGraph(ret.tolist())
    print(ret)


def test_extend():
    # 测试
    G = generate_complete_graph(30)
    T = generate_tree(G, 4)
    result = expand_tree(G, T)
    print(result)

    plot.visulizeGraph(G.tolist())
    plot.visulizeGraph(T.tolist())
    plot.visulizeGraph(result.tolist())


if __name__ == "__main__":
    test_extend()