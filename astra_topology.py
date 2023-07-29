import networkx as nx
import numpy as np
from config import logger
import plot
import config


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
                new_over_nodes = [
                    n for n in T.nodes() if T.degree(n) > max_degree]

                new_overflow = overflow_degree(T, new_over_nodes, max_degree)
                logger.debug(f"the new_overflow is {new_overflow}")

                if new_overflow < old_overflow and (nx.is_connected(T)):
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


def shortest_paths(node, adj_matrix):
    # 邻接矩阵转换成numpy array
    adj_matrix = np.array(adj_matrix)
    # 创建图
    G = nx.from_numpy_array(adj_matrix)

    # 创建一个空的结果列表
    result = []

    # 对于图中的每个节点
    for target in G.nodes:
        # 如果目标节点不是输入节点
        if target != node:
            # 计算并保存最短路径
            path = nx.shortest_path(G, source=node, target=target)
            result.append(path)

    return result


def from_index_to_dic(shortest_path):
    # 注意此时path里面就只有一条路径，后面再考虑添加多条路径
    response_data = {}
    for i, path in enumerate(shortest_path):
        key = config.NodeList[path[-1]]
        response_data[key] = []
        tmp = []
        for node_index in path:
            tmp.append(config.NodeList[node_index])
        response_data[key].append((":").join(tmp))
    return response_data


def get_subgraphs(G):
    # 这个函数暂时先不要用，留在这里仅仅为了有一些有用的 snippets
    G = nx.from_numpy_matrix(G)
    # 找到图中所有连通组件的节点列表
    components = list(nx.connected_components(G))
    # 初始化一个空列表来存储子图邻接矩阵和节点映射
    subgraphs_adj_matrix = []
    subgraphs_mapping = []
    # 对于每个连通组件
    for component in components:
        # 提取子图
        subgraph = G.subgraph(component)
        # 转换为邻接矩阵并存储
        adj_matrix = nx.to_numpy_matrix(subgraph).tolist()
        subgraphs_adj_matrix.append(adj_matrix)
        # 将节点映射存储为一个字典，其中原始图中的节点索引是键，子图中的新索引是值
        mapping = {node: i for i, node in enumerate(component)}
        subgraphs_mapping.append(mapping)
    return subgraphs_adj_matrix, subgraphs_mapping


def get_certain_subgraph(index, G):
    # 这个函数用来获得指定index所在的子图，以及返回子图和原图之间的mapping关系
    G = nx.from_numpy_matrix(G)
    # 找到图中所有连通组件的节点列表
    components = list(nx.connected_components(G))

    # 对于每个连通组件
    for component in components:
        if index not in component:
            continue
        # 提取子图
        subgraph = G.subgraph(component)
        # 转换为邻接矩阵并存储
        adj_matrix = nx.to_numpy_matrix(subgraph).tolist()
        # 将节点映射存储为一个字典，其中原始图中的节点索引是键，子图中的新索引是值
        mapp_from_sub_to_original = {
            node: i for node, i in enumerate(component)
        }

        map_form_original_to_sub = {
            node: i for i, node in enumerate(component)
        }
        return adj_matrix, mapp_from_sub_to_original, map_form_original_to_sub


def index_mapping(shortest_path, mapping):
    # 这个函数用来将shortest_path中的index转换为原始的index
    # 其中 shortest_path是一个[[], [], []]的数组
    # 其中mapping是一个字典
    for path in shortest_path:
        for i, node in enumerate(path):
            path[i] = mapping.get(node)
    return shortest_path


def traditional_topology(graph_list, max_degree=4):
    graph = np.array(graph_list)
    # 创建一个空的邻接矩阵E，-1表示不可达
    E = -np.ones(graph.shape)
    
    # 获取顶点数量
    vertices_num = len(graph)

    # 初始化每个顶点的度为0
    degree = [0]*vertices_num

    # 获得边和对应的权重
    edges = []
    for i in range(vertices_num):
        for j in range(i+1, vertices_num):
            if graph[i, j] >= 0:
                edges.append(((i, j), graph[i, j]))
    
    # 按照权重对边进行排序
    edges.sort(key=lambda x: x[1])
    
    for edge, _ in edges:
        u, v = edge
        # 检查添加边后顶点的度是否超过4
        if degree[u] < 4 and degree[v] < 4:
            E[u, v] = E[v, u] = graph[u, v]
            degree[u] += 1
            degree[v] += 1
    
    return E.tolist()


def astra_topology(graph_list, max_degree=4):
    graph = np.array(graph_list)
    T = generate_tree(graph, max_degree)
    res = expand_tree(graph, T)
    return res.tolist()