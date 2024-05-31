import requests
from datetime import datetime, timedelta
import json

# 获取前一天的日期字符串
def get_yesterday_date():
    yesterday = datetime.now() - timedelta(1)
    start_date = yesterday.strftime("%Y-%m-%d 00:00:00")
    end_date = yesterday.strftime("%Y-%m-%d 23:59:59")
    return start_date, end_date

# 获取 observation 数据
def fetch_observations_for_date(date):
    url = "https://apis.ecan.govt.nz/waterdata/observations/graphql"
    start_date = date.strftime("%Y-%m-%d 00:00:00")
    end_date = date.strftime("%Y-%m-%d 23:59:59")
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
        'Authorization': '6edbcd8d814148468015d7d63219434c'  # 替换为你的API密钥
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
        # 将数据保存到本地文件
        file_path = f"/home/ubuntu/app/{date.strftime('%Y%m%d')}.json"
        with open(file_path, 'w') as file:
            json.dump(observations, file)
        return observations
    else:
        print("Failed to fetch data")
        return None

if __name__ == "__main__":
    yesterday = datetime.now() - timedelta(1)
    fetch_observations_for_date(yesterday)
