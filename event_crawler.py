# -*- coding: utf-8 -*-
# Title : crawling event data in pathetic old Korean marathon website
# Website : http://www.roadrun.co.kr/schedule/
# Korean : 마라톤 웹사이트 이벤트(2016부터) 데이터 크롤링
# Written by : @sujinleeme
# Date : 2017. 04. 08.

import re
import datetime
import requests
import json
import forecastio
from bs4 import BeautifulSoup

today = datetime.datetime.now()
print('Working Date : {}'.format(today))

# count total annual event
def count_annual_event():
    baseUrl = "http://www.roadrun.co.kr/schedule/list.php?today=1451574000&todays=Y"
    read = requests.get(baseUrl)
    soup = BeautifulSoup(read.content, 'html.parser')
    try:
        table = soup.find('body').find_all('table')[10:11]
        trs = [tr for tr in table][0].find_all('tr')
        total = int(len(trs)/2)
        if total <= 1:
            table = soup.find('body').find_all('table')[11:12]
            trs = [tr for tr in table][0].find_all('tr')
            total = int(len(trs)/2)
            print("Ready to crawl {} marathon events since 2017.".format(total))
    except:
        print("Can't crawl data from website.")
    return(total)


def extract_event_data(url):
    read = requests.get(str(url))
    soup = BeautifulSoup(read.content, 'html.parser', from_encoding='euc-kr')
    table = soup.find_all('table')[1]
    info = [s.strip() for s in table.text.splitlines() if s]
    info = list(filter(None, info))[1::2]
    info[11:len(info)] = [' '.join(info[11:len(info)])]
    return(info)

def execute_crawling(start):
    #store all data in empty list
    all_data = []
    total = int(count_annual_event())
    #get final URL query
    end = int(start) + total
    print("Collecting data... wait for a minute.")
    try:
        for i in range(start, end):
            url = 'http://www.roadrun.co.kr/schedule/view.php?no={}'.format(i)
            new_data = extract_event_data(url) #values
            if len(new_data) != 9:
                all_data.append(new_data)
        print("Merge all events data...")
    except:
        print("Fail to read contents")
    print("{} events are empty.".format(total-len(all_data)))
    all_data = data_formatting(all_data)
    result = dict([("2017", all_data)])
    return(result)

def data_formatting(data):
    keys = ["title", "host", "email", "date", "phone", "race", "city",
            "location", "host", "application_period", "website", "description",
            "latitude", "longitude", "map_url", "temperature", "weather"]
    data = [x.replace(x, '.') if x in keys else x for x in data]
    #formatted date string:
    for i in range(len(data)):
        elem = data[i]
        dateList = change_datalist_type(elem[3])
        elem = format_date_str(elem, dateList)
        elem[5] = change_racelist_type(elem[5])
        location = re.sub(',', ' ', elem[7])
        #get map data
        geocode = fetch_location(location)
        #get weather data
        weather = fetch_weather(geocode[0], geocode[1], dateList)
        elem = [*elem, *geocode, *weather]
        elem = dict(zip(keys, elem))
        data[i] = elem
    data = sorted(data, key=lambda k: k['date'], reverse=True)
    print('Data formatting...')
    return(data)

# Make date string to list type to get geocode location
def change_datalist_type(date):
    dateList = re.findall('\d+', date)[:5]
    # Fix wrong user input
    # Covert 12 hour to 24 hour
    hourStr = dateList[3]
    if '오후' in hourStr:
        dateList[3] += 12
    if len(str(hourStr))==4:
        dateList[3] = str(hourStr)[::2]

    dateList = list(map(int,dateList))
    return(dateList)

def format_date_str(data, date):
    data[3] = datetime.datetime(*date).strftime("%Y/%m/%d %H:%M")
    #formatted 'application_period' e.g)2017/01/01 - 2017/04/04
    try:
        data[9] = '{}/{}/{} - {}/{}/{}'.format(*(re.findall('\d+', data[9])))
    except IndexError:
        print("Found unexpected 'application_period' type. But it will be ignored.")
        pass
    return(data)

# Daum map API
def fetch_location(place):
    baseUrl = 'https://apis.daum.net/local/v1/search/keyword.json'
    params = {'apikey':'317394cebdea4b6359a849bcf994be38', 'sort':1, 'query':place}
    content = requests.get(baseUrl, params=params).json()
    mapData = content['channel']['item']
    try:
        if len(mapData) == 0: #can't search place
            place = ' '.join(place.split()[:-1])
            return (fetch_location(place))
        else:
            mapData = mapData[0]
            map_list = [mapData['latitude'], mapData['longitude'], 'http://map.daum.net/link/map/{}'.format(mapData['id'])]
            return (map_list)
    except KeyError:
        map_list = ['', '', '']
        return (map_list)

# forcase.io API
def fetch_weather(latitude, longitude, date):
    apikey = 'd5e9ae1a96b8e4a1509ceba9e8ebd92d'
    formatted_date = datetime.datetime(*date)
    if len(longitude) == 0:
        weather_list = ['', 'null']
        return(weather_list)
    else:
        try:
            forecast = forecastio.load_forecast(apikey, latitude, longitude, time=formatted_date)
            weather = forecast.currently()
            weather_list = [('{}°C'.format(weather.temperature)), weather.icon]
            return(weather_list)
        except:
            weather_list = ['', 'null']
            return(weather_list)

def change_racelist_type(race):
    race = [x.strip() for x in race.split(',')]
    race = dict(enumerate(race))
    return(race)

# read evevnt data since first event in 2017
# year first event http://www.roadrun.co.kr/schedule/view.php?no=6565

result_crawled = (execute_crawling(6565))
print("Ready to save {} events in file".format(len(result_crawled)))

jsonObj = json.dumps(result_crawled, ensure_ascii=False, indent=4)

#save file
with open("/json-sample/2017Event.json", "w") as f:
    try:
        f.write(jsonObj)
        print("Updated all data successfully 2017Event.json!")
    except:
        print("ERROR: event_data.py can't be updated.")
