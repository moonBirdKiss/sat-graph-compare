import grakel as gk
import numpy as np
from config import logger
import plot
import skyfield.api
import constellation
from config import logger
import config
import graphTools


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


# 测试
if __name__ == "__main__":
    logger.info("Staring to test graph similarity")
    graph_similartiy_node_varies(20)
    logger.info("Test graph similarity finished")
