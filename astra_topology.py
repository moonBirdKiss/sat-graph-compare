import networkx as nx
import numpy as np
from config import logger
import plot

def get_connected_subgraph_adj_matrices(adj_matrix):
    # 这个函数也有用，用来做最初的状态
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
    logger.debug(f"the over_nodes is {over_nodes}")

    while over_nodes:
        old_overflow = overflow_degree(T, over_nodes, max_degree)
        logger.debug(f"The old_overflow is {old_overflow}")
        v = over_nodes.pop()  # 取一个超度节点
        neighbors = list(T.neighbors(v))  # 获得它的邻居节点
        logger.debug(f"the neighbors is {neighbors}")
        
        flag = False
        
        for u in neighbors:
            # plot.visulizeGraph(nx.to_numpy_matrix(T).tolist())
            logger.debug(f" remove edge {(u, v)}")

            T.remove_edge(u, v)  # 删除一条连接边

            E = set(G.edges()) - set(T.edges())  # 剩余可用边集合
            logger.debug(f"the E is {E}")
            for e in E:
                logger.debug(f"try to add edge {e}")
                # 尝试添加边,检查是否符合要求
                T.add_edge(*e)

                # plot.visulizeGraph(nx.to_numpy_matrix(T).tolist())
                new_over_nodes = [n for n in T.nodes() if T.degree(n) > max_degree]
                
                new_overflow = overflow_degree(T, new_over_nodes, max_degree)
                logger.debug(f"the new_overflow is {new_overflow}")

                if  new_overflow < old_overflow and (nx.is_connected(T)):
                    logger.debug(f"find a suitable edge {e}")
                    flag = True
                    break  # 找到符合的边,退出e循环
                else:
                    T.remove_edge(*e)  # 否则删除边


            if flag:
                break  # 找到符合的边,退出u循环
            
            logger.debug(f"back to add edge {(u,v)}")
            T.add_edge(u, v)  # 没找到符合的边,回退操作


        if max([T.degree(n) for n in T.nodes()]) <= max_degree:
            logger.debug(f"Loop stop")
            break  # 找到符合的边,跳出v循环
        logger.debug(f"Loop continue, current is {v}")

        over_nodes = [n for n in T.nodes()
                      if T.degree(n) > max_degree]  # 更新超度节点列表

    return nx.to_numpy_matrix(T)  # 返回结果矩阵


def overflow_degree(G, over_nodes, max_degree):
    overflow_metric = 0
    for v in over_nodes:
        overflow_metric += G.degree(v) - max_degree
    return overflow_metric



def expand_tree(graph_matrix, tree_matrix):
    # 将邻接矩阵转换为图
    G_graph = nx.from_numpy_matrix(np.array(graph_matrix))
    T_graph = nx.from_numpy_matrix(np.array(tree_matrix))

    # 计算G-T得到的边集合E
    E = list(set(G_graph.edges()).difference(set(T_graph.edges())))

    # 将E中的边尽可能的添加到T上，但需要保证T的每一个顶点的度小于或等于4
    # 同时添加边的顺序从T中度最小的顶点开始
    for edge in sorted(
            E, key=lambda x: min(T_graph.degree(x[0]), T_graph.degree(x[1]))):
        if T_graph.degree(edge[0]) < 4 and T_graph.degree(edge[1]) < 4:
            T_graph.add_edge(*edge)

    return nx.to_numpy_matrix(T_graph)


def astra_topology(adj_matrix, max_degree=4):
    # 生成树
    tree_matrix = generate_tree(adj_matrix, max_degree)
    # 扩展树
    result = expand_tree(adj_matrix, tree_matrix)
    return result.tolist()