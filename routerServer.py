from flask import Flask, request, jsonify
from config import logger
import constellation
import skyfield.api

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


@app.route('/gs-communication', methods=['POST'])
def communication():
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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
