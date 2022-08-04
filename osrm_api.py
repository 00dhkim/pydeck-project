import requests
import json
import pandas as pd


# 출발좌표, 도착좌표로 최단거리 route 제공
def get_route(coord, start_time=0):
    # coord: [[start_lat, start_lng], [end_lat, end_lng]]
    start_lat, start_lng = coord[0]
    end_lat, end_lng = coord[1]
    
    url = 'http://router.project-osrm.org/route/v1/driving/'
    url += str(start_lat) + ',' + str(start_lng) + ';'
    url += str(end_lat) + ',' + str(end_lng)
    url += '?overview=false&steps=true'
    response = requests.get(url)
    data = response.json()
    
    # print(len(data['routes'][0]['legs'][0]['steps']))
    locations = []
    timestamps = []
    timestamp = 0 + start_time
    
    for step in data['routes'][0]['legs'][0]['steps']:
        timestamp += step['duration'] % 86400 # 24시간을 넘어가면 다시 0으로 돌림
        locations.append(step['maneuver']['location'])
        timestamps.append(timestamp)
    
    df = pd.DataFrame([{
        'path': locations,
        'timestamp': timestamps
    }])
    
    return df