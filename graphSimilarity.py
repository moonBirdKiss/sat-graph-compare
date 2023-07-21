import grakel as gk
import numpy as np
from config import logger
import plot
import skyfield.api
import constellation
from config import logger
import config 


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


def sats_grakel(sats_grahp1, sats_grahp2):
    # 将这些邻接矩阵转换为GraKeL Graph格式

    g1 = gk.Graph(sats_grahp1, node_labels={
                  i: 1 for i in range(len(sats_grahp1))}
                  )

    g2 = gk.Graph(sats_grahp2, node_labels={
                  i: 1 for i in range(len(sats_grahp2))}
                  )

    # 计算各种核的相似性
    for kernel in ['shortest_path', 'graphlet_sampling', 'weisfeiler_lehman']:
        graph = gk.GraphKernel(kernel=kernel, normalize=True)
        K = graph.fit_transform([g1, g2])
        logger.info(f"{kernel} similarity: {K[0,1]}")


def test():
    c = constellation.new_sats()
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 29)
    g1 = c.sat_connectivity(dt)

    # 比较 0 - 300 的结果
    for i in range(config.iteration_time):
        # the sacle 
        j = i * config.time_scale
        dt = ts.utc(2023, 7, 20, 12, 20 + j // 60, 29 + j % 60)
        g2 = c.sat_connectivity(dt)
        res = sats_grakel(g1, g2)
        # logger.info(f"index:{i}, result: {res} type: {type(res)}")


if __name__ == "__main__":
    test()
