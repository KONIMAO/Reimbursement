# /System/Library/Frameworks/Python.framework/Versions/2.7/Resources/Python.app/Contents/MacOS/Python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import strip

import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate('./fir-demo-9b0ef-firebase-adminsdk-477he-90a13b90ea.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://fir-demo-9b0ef-default-rtdb.firebaseio.com/',
})

# ref = db.reference('transit')
# ref.set({
#     '1': {
#         'departure': '東京',
#         'destination': '大阪'
#     },
#     '2': {
#         'departure': '東京',
#         'destination': '名古屋'
#     }
# })

# print (ref.get('/departure'))

#出発駅の入力
departure_station = input('出発駅：')
#到着駅の入力
destination_station = input('到着駅：')

#経路の取得先URL
route_url = "https://transit.yahoo.co.jp/search/print?from="+departure_station+"&flatlon=&to="+ destination_station+"&type=5&s=0&ws=3&expkind=2&ticket=ic&y=2022&m=05&d=28&hh=23&m1=5&m2=5&no=1&fromgid=&togid=&tlatlon=&via=&viacode=&userpass=1&al=0&shin=1&ex=1&hb=0&lb=0&sr=0"
print(route_url)
#Requestsを利用してWebページを取得する
route_response = requests.get(route_url)

# BeautifulSoupを利用してWebページを解析する
route_soup = BeautifulSoup(route_response.text, 'html.parser')

#経路のサマリーを取得
route_summary = route_soup.find("div",class_ = "routeSummary")
#所要時間を取得
required_time = route_summary.find("li",class_ = "time").get_text()
#乗り換え回数を取得
transfer_count = route_summary.find("li", class_ = "transfer").get_text()
#料金を取得
fare = route_summary.find("li", class_ = "fare").get_text()

print("======"+departure_station+"から"+destination_station+"=======")
print("所要時間："+required_time)
print(transfer_count)
print("料金："+fare)

#乗り換えの詳細情報を取得
route_detail = route_soup.find("div",class_ = "routeDetail")

#乗換駅の取得
stations = []
stations_tmp = route_detail.find_all("div",class_="station")
for station in stations_tmp:
    stations.append(station.get_text().strip())

#乗り換え路線の取得
lines = []
lines_tmp = route_detail.find_all("li", class_="transport")
for line in lines_tmp:
    line = line.find("div").get_text().strip() # hennkou
    lines.append(line)

#路線ごとの所要時間を取得
estimated_times = []
estimated_times_tmp = route_detail.find_all("li", class_="estimatedTime")
for estimated_time in estimated_times_tmp:
    estimated_times.append(estimated_time.get_text())

print(estimated_times)

#路線ごとの料金を取得
fars = []
fars_tmp = route_detail.find_all("p", class_="fare")
for fare in fars_tmp:
    fars.append(fare.get_text().strip())


#乗り換え詳細情報の出力
print("======乗り換え情報======")
for station,line,estimated_time,fare in zip(stations,lines,estimated_times,fars):
    print(station)
    print( " | " + line + " " + estimated_time + " " + fare)
print(stations[len(stations)-1])
