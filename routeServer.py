from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/communication', methods=['POST'])
def communication():
    print(request.json)  # 打印请求的JSON
    data = [
        [(0, 0, 0), (1, 100.5, 20), (1, 120.5, 30)],
        [(1, 100.5, 20), (0, 0, 0), (0, 0, 0)],
        [(1, 120.5, 30), (0, 0, 0), (0, 0, 0)]
    ]
    return jsonify(data)  # 返回数据

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
