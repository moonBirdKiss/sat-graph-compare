import requests

url = 'http://127.0.0.1:8000/communication'

payload = {
    "size": 3,
    "time": 40
}

response = requests.post(url, json=payload)

print(response.json())  # 打印服务器返回的数据
