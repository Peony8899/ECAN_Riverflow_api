import requests
from flask import Flask, jsonify
from datetime import datetime
import json
import os

application = Flask(__name__)

# 读取本地JSON文件并加载数据
def load_data(file_path):
    if not os.path.exists(file_path):
        return None  # 文件不存在时返回None
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

# 获取 observation 数据
def fetch_observations_for_date(date_str):
    url = "https://apis.ecan.govt.nz/waterdata/observations/graphql"
    start_date = f"{date_str} 00:00:00"
    end_date = f"{date_str} 23:59:59"
    query = f"""
    query {{
        getObservations {{
            locationId
            observations(filter: {{ start: "{start_date}", end: "{end_date}" }}) {{
                qualityCode
                timestamp
                value
            }}
        }}
    }}
    """
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '6edbcd8d814148468015d7d63219434c'  # 替换为你的API密钥
    }
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        observations = []
        for observation in data['data']['getObservations']:
            location_id = observation['locationId']
            for record in observation['observations']:
                observations.append({
                    'locationId': location_id,
                    'qualityCode': record['qualityCode'],
                    'timestamp': record['timestamp'],
                    'value': record['value']
                })
        return observations
    else:
        print("Failed to fetch data from API", response.status_code, response.text)
        return None

# 路由：获取元数据
@application.route('/pwa115/get_locations')
def get_metadata():
    data = load_data('/home/ubuntu/app/meta.json')  # 确保路径正确
    if data is None:
        return jsonify({"error": "Meta data not available"}), 404
    return jsonify(data)

# 路由：获取 observation 数据
@application.route('/pwa115/get_observations/<date_str>')
def get_observations(date_str):
    try:
        # 将日期字符串转换为带短线的标准格式
        date = datetime.strptime(date_str, '%Y%m%d').strftime('%Y-%m-%d')
        observations = fetch_observations_for_date(date)
        if observations:
            return jsonify(observations)
        else:
            return jsonify({"error": "Failed to fetch data from API"}), 500
    except ValueError:
        return jsonify({"error": "Invalid date format"}), 400

# 路由：默认欢迎信息
@application.route("/")
def welcome():
    return jsonify({"message": "Hello, World!"})

if __name__ == '__main__':
    application.run(host='0.0.0.0', port=8000)
