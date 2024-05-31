import requests
from datetime import datetime, timedelta
import json
import os

# 获取前一天的日期字符串
def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    start_date = yesterday.strftime("%Y-%m-%d 00:00:00")
    end_date = yesterday.strftime("%Y-%m-%d 23:59:59")
    return start_date, end_date

# 获取 observation 数据
def fetch_observations():
    url = "https://apis.ecan.govt.nz/waterdata/observations/graphql"
    start_date, end_date = get_yesterday_date()
    query = f"""
    query {{
        getObservations {{
            locationId
            name
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
        'Authorization': '6edbcd8d814148468015d7d63219434c'  # 替换为你的API密钥
    }
    response = requests.post(url, json={'query': query}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # 将数据保存到本地文件
        with open('/home/ubuntu/app/observations.json', 'w') as file:
            json.dump(data, file)
    else:
        print("Failed to fetch data")

if __name__ == "__main__":
    fetch_observations()
