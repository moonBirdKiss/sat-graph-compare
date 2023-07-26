import grakel as gk
import numpy as np
from config import logger
import plot
import skyfield.api
import constellation
from config import logger
import config
import graphTools
import networkx as nx


def tutorial_grakel():
    # 创建两个图的邻接矩阵
    A1 = np.array([
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    ])

    A2 = np.array([
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0]
    ])

    # 创建图对象
    g1 = gk.Graph(np.array(A1), node_labels={i: 1 for i in range(len(A1))})
    g2 = gk.Graph(np.array(A2), node_labels={i: 1 for i in range(len(A2))})

    # 计算各种核的相似性
    for kernel in ['shortest_path', 'graphlet_sampling', 'weisfeiler_lehman', 'subtree_wl']:
        graph = gk.GraphKernel(kernel=kernel, normalize=True)
        K = graph.fit_transform([g1, g2])
        logger.info(f"{kernel} similarity: {K[0,1]}")


def sats_grakel(sats_grahp1, sats_grahp2, kernel):
    # 计算各种核的相似性
    g1 = gk.Graph(np.array(sats_grahp1))
    g2 = gk.Graph(np.array(sats_grahp2))
    kernel.fit_transform([g1])
    res = kernel.transform([g2])
    return res[0][0]


def graph_similarity_time_varies(size=config.Constellation_scale, iter_time=config.iteration_time, time_scale=config.time_scale):
    c = constellation.new_sats(size)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)
    g1 = c.sat_connectivity(dt)

    # prepare three lists and three kernels
    sp_kernel = gk.ShortestPath(normalize=True, with_labels=False)
    sp_res = []

    rw_kernel = gk.RandomWalk(normalize=True, kernel_type='exponential')
    rw_res = []

    gs_kernel = gk.GraphletSampling(normalize=True, k=5)
    gk_res = []
    # 比较 0 - 300 的结果
    for i in range(iter_time):
        logger.info(f"{i}, never be annoying")
        # the sacle
        j = i * time_scale
        dt = ts.utc(2023, 7, 20, 12, 20 + j // 60, 29 + j % 60)
        g2 = c.sat_connectivity(dt)

        sp_res.append(sats_grakel(g1, g2, sp_kernel))
        rw_res.append(sats_grakel(g1, g2, rw_kernel))
        gk_res.append(sats_grakel(g1, g2, gs_kernel))

    # save the res
    graphTools.save_file("sp_res.txt", sp_res)
    graphTools.save_file("rw_res.txt", rw_res)
    graphTools.save_file("gk_res.txt", gk_res)


def graph_similartiy_node_varies(size=config.Constellation_scale):
    # this method is used to compare the similarity of graph when the number of
    # satellite varies, try to prove the small number will incurre the high variation
    # while the large satellite number can reduce the variation
    graph_similarity_time_varies(size)
    pass


def compare_adjacency_matrices(matrx1, matrx2):
     # 将输入的列表转换为numpy数组以进行计算
    matrix1 = np.array(matrx1)
    matrix2 = np.array(matrx2)

    # 检查两个矩阵是否形状相同
    if matrix1.shape != matrix2.shape:
        print("Error: The two matrices must be the same size.")
        return None

    # 计算两个矩阵的差异
    difference = np.abs(matrix1 - matrix2)
    # 计算差异矩阵中所有非零元素的数量，即边的变化数量
    change_count = np.count_nonzero(difference)
    # 因为是无向图，所以返回值除以2
    change_count //= 2

    return change_count   



def common_subgraph(matrices):
    # 将输入的列表转换为numpy数组以进行计算
    matrices = np.array(matrices)

    # 检查所有矩阵是否形状相同
    for i in range(len(matrices) - 1):
        if matrices[i].shape != matrices[i+1].shape:
            print("Error: All matrices must be the same size.")
            return None

    # 计算所有邻接矩阵的逐元素最小值
    common_matrix = np.min(matrices, axis=0)

    return common_matrix



def write_list_to_file(lst, path_file):
    # 打开文件
    with open(path_file, 'w') as f:
        # 遍历列表中的每个元素
        for item in lst:
            # 将元素写入文件中
            f.write(f'{item}\n')


def common_subgraph(matrices):
    # 将输入的列表转换为numpy数组以进行计算
    matrices = np.array(matrices)

    # 检查所有矩阵是否形状相同
    for i in range(len(matrices) - 1):
        if matrices[i].shape != matrices[i+1].shape:
            print("Error: All matrices must be the same size.")
            return None

    # 计算所有邻接矩阵的逐元素最小值
    common_matrix = np.min(matrices, axis=0)

    return common_matrix.tolist()

def is_connected(adj_matrix):
    # 将邻接矩阵转为 numpy array
    adj_matrix = np.array(adj_matrix)
    
    # 通过 networkx 将 numpy array 转为图对象
    G = nx.from_numpy_array(adj_matrix)
    
    # 判断图是否连通并返回结果
    return nx.is_connected(G)