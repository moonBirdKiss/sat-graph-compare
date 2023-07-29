from config import logger
from astra_topology import *
import numpy as np
import plot
import matplotlib.pyplot as plt


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


def test_shortest_path():
    # 测试函数
    G = generate_complete_graph(8)
    T = generate_tree(G, 4)
    result = expand_tree(G, T)
    adj_matrix = result.tolist()
    res = shortest_paths(0, adj_matrix)
    print(res)
    plot.visulizeGraph(adj_matrix)

    dic = from_index_to_dic(res)
    logger.info(f"dic: {dic}")


def test_sub_mapp():
    # 创建一个包含两个连通子图的随机图
    G = nx.connected_watts_strogatz_graph(10, 3, 0.1)
    H = nx.connected_watts_strogatz_graph(10, 3, 0.1)
    G = nx.disjoint_union(G, H)

    # 画出原始图
    plt.figure(figsize=(6, 6))
    plt.title('Original Graph')
    nx.draw(G, with_labels=True)

    # 获取子图
    subgraphs_adj_matrix, subgraphs_mapping = get_subgraphs(
        nx.to_numpy_matrix(G))

    # 画出子图
    for i, (adj_matrix, mapping) in enumerate(zip(subgraphs_adj_matrix, subgraphs_mapping)):
        subgraph = nx.from_numpy_array(np.array(adj_matrix))
        plt.figure(figsize=(6, 6))
        plt.title(f'Subgraph {i+1}')
        nx.draw(subgraph, with_labels=True)
        print(f'Subgraph {i+1} Mapping: {mapping}')
    plt.show()


def test_certain_subgraph():
    # 创建一个包含两个连通子图的随机图
    G = nx.connected_watts_strogatz_graph(10, 3, 0.1)
    H = nx.connected_watts_strogatz_graph(10, 3, 0.1)
    G = nx.disjoint_union(G, H)

    # 画出原始图
    plt.figure(figsize=(6, 6))
    plt.title('Original Graph')
    nx.draw(G, with_labels=True)

    # 获取子图
    adj_matrix, map_from_new_to_old, map_from_old_to_new = get_certain_subgraph(
        12, nx.to_numpy_matrix(G))
    subgraph = nx.from_numpy_array(np.array(adj_matrix))

    # 画出子图
    plt.figure(figsize=(6, 6))
    nx.draw(subgraph, with_labels=True)
    plt.title('Original Graph')

    # 获得最短路径
    path = shortest_paths(0, adj_matrix)
    print(path)
    # 然后返回的顶点
    res = index_mapping(path, map_from_new_to_old)
    print(res)
    plt.show()



def test_traditional_topolog():
    G = generate_complete_graph(30)
    T = traditional_topology(G.tolist())
    plot.visulizeGraph(T)


if __name__ == "__main__":
    test_traditional_topolog()
