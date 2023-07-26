import networkx as nx
import numpy as np
from config import logger


def get_connected_subgraph_adj_matrices(adj_matrix):
    G = nx.from_numpy_matrix(adj_matrix)
    subgraphs = nx.connected_components(G)

    subgraph_adj_matrices = [
        nx.to_numpy_matrix(G.subgraph(subgraph)) for subgraph in subgraphs
    ]
    return subgraph_adj_matrices


def get_minimum_spanning_tree(adj_matrix):
    # 创建一个图
    G = nx.from_numpy_matrix(adj_matrix)

    # 计算最小生成树
    mst = nx.minimum_spanning_tree(G)

    # 将最小生成树转换为邻接矩阵
    mst_adj_matrix = nx.to_numpy_matrix(mst)

    return mst_adj_matrix


def find_max_degree_node(adj_matrix):
    # 创建一个图
    G = nx.from_numpy_matrix(adj_matrix)

    # 找到度最大的节点
    max_degree_node = max(G, key=G.degree)

    return max_degree_node


def get_max_degree_node(adj_matrix):
    # 获得度最大的节点
    # 但是上面的方法更加优雅
    G = nx.from_numpy_matrix(adj_matrix)
    degrees = [val for (node, val) in G.degree()]
    max_degree = max(degrees)
    for node, degree in G.degree():
        if degree == max_degree:
            return node


def generate_complete_graph(nodenum):
    G = nx.complete_graph(nodenum)
    return nx.to_numpy_matrix(G)


def generate_tree(graph_matrix, max_degree=4):

    G = nx.from_numpy_matrix(graph_matrix)  # 从矩阵创建图G
    T = nx.minimum_spanning_tree(G)  # 求最小生成树T
    over_nodes = [n for n in T.nodes() if T.degree(n) > max_degree]  # 找到超度节点

    while over_nodes:
        v = over_nodes.pop()  # 取一个超度节点
        neighbors = list(T.neighbors(v))  # 获得它的邻居节点

        for u in neighbors:
            T.remove_edge(u, v)  # 删除一条连接边
            T1, T2 = get_connected_subgraph_adj_matrices(
                nx.to_numpy_matrix(T))  # 获得最大连通子图
            T1 = nx.from_numpy_matrix(T1)  # 转换为图
            T2 = nx.from_numpy_matrix(T2)  # 转换为图
            E = set(G.edges()) - set(T1.edges()) - set(T2.edges())  # 剩余可用边集合
            for e in E:
                # 尝试添加边,检查是否符合要求
                T.add_edge(*e)
                if max([T.degree(n) for n in T.nodes()]) <= max_degree:
                    break  # 找到符合的边,退出循环
                else:
                    T.remove_edge(*e)  # 否则删除边

            if max([T.degree(n) for n in T.nodes()]) <= max_degree:
                break  # 找到符合的边,跳出u循环
            T.add_edge(u, v)  # 没找到符合的边,回退操作

        if T.degree(v) > max_degree:
            logger.error(f"Error: Can't find a suitable edge for node {v}")
            break
        else:
            logger.info(f"Find a suitable edge for node {v}")

        if max([T.degree(n) for n in T.nodes()]) <= max_degree:
            break  # 找到符合的边,跳出v循环

        over_nodes = [n for n in T.nodes()
                      if T.degree(n) > max_degree]  # 更新超度节点列表

    return nx.to_numpy_matrix(T)  # 返回结果矩阵
