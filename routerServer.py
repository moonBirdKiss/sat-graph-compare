from flask import Flask, request, jsonify
from config import logger
import constellation
import skyfield.api
import astra_topology
import numpy as np
import plot
import networkx as nx
import config


app = Flask(__name__)


@app.route('/communication', methods=['POST'])
def communication():
    print(request.json)  # 打印请求的JSON
    query_time = request.json.get('time')
    size = request.json.get('size')
    logger.debug(f"query_time:{query_time}, size:{size}")

    # 构建constellation，然后返回对应的值
    sats = constellation.new_sats(size)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 30 + query_time)

    res = sats.sat_connection(dt)
    # logger.info(res)

    return jsonify(res)  # 返回数据


@app.route('/connectivity', methods=['POST'])
def connectivity():
    print(request.json)  # 打印请求的JSON
    query_time = request.json.get('time')
    size = request.json.get('size')
    logger.debug(f"query_time:{query_time}, size:{size}")

    # 构建constellation，然后返回对应的值
    sats = constellation.new_sats(size)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 30 + query_time)

    res = sats.sat_connectivity(dt)
    # logger.info(res)

    return jsonify(res)  # 返回数据


@app.route('/gs-communication', methods=['POST'])
def gs_communication():
    # return the gs information
    print(request.json)  # 打印请求的JSON
    query_time = request.json.get('time')
    size = request.json.get('size')
    logger.debug(f"query_time:{query_time}, size:{size}")

    # 构建constellation，然后返回对应的值
    sats = constellation.new_sats(size)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 30 + query_time)

    res = sats.gs_connection(dt)
    # logger.info(res)

    return jsonify(res)  # 返回数据


@app.route('/gs-connectivity', methods=['POST'])
def gs_connectivity():
    # return the gs information
    print(request.json)  # 打印请求的JSON
    query_time = request.json.get('time')
    size = request.json.get('size')
    logger.debug(f"query_time:{query_time}, size:{size}")

    # 构建constellation，然后返回对应的值
    sats = constellation.new_sats(size)
    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 30 + query_time)

    res = sats.gs_connectivity(dt)
    # logger.info(res)

    return jsonify(res)  # 返回数据


@app.route('/sat-route-update', methods=['POST'])
def sat_route_update():
    data = request.get_json()
    # data should be a dict with keys: index, sat_size, ground_size
    logger.info(f"Received data: {data}")

    sat_size = data.get('sat_size')
    ground_size = data.get("ground_size")
    index = data.get('index')

    # 构建constellation，然后返回对应的值
    c = constellation.new_sats(sat_size, ground_size)

    ts = skyfield.api.load.timescale()
    dt = ts.utc(2023, 7, 20, 12, 20, 30)

    # 只需得到连通性就可以了
    gs_connectivity = c.gs_connectivity(dt)

    logger.info(f"original: {gs_connectivity}")

    gs_connectivity, new_to_old, old_to_new = astra_topology.get_certain_subgraph(index,
                                                                                  np.array(gs_connectivity))

    mortify_matrix = astra_topology.astra_topology(
        np.array(gs_connectivity), 4)
    logger.info(f"mortify: {mortify_matrix}")

    # 然后从相关的矩阵中构建path提供给edgemesh
    shorest_path = astra_topology.shortest_paths(
        old_to_new.get(index), mortify_matrix)

    logger.info(f"shorest_path: {shorest_path}")

    # 利用mapping，将node的值变回去
    res = astra_topology.index_mapping(shorest_path, new_to_old)
    logger.info(f"res: {res}")

    dic = astra_topology.from_index_to_dic(res)
    logger.info(f"dic: {dic}")

    return jsonify(dic)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
