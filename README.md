# KoreaMarathonAPI
2017 Korea Marathon Events Web-Crawling

[마라톤 온라인](http://www.marathon.pe.kr/schedule_index.html)의 2017년도 마라톤 행사를 크롤링하여 API로 만들었습니다. 
기존 정보 이외에 지도(위도, 경도), 다음지도URL, 기온, 날씨아이콘타입 정보를 제공합니다.
원 사이트에서 올바르지 않은 데이터가 있을 시, 지도정보(도시명, 위도, 경도)와 날씨정보(기온, 날씨아이콘)이 표시되지 않을 수 있습니다.
대회일시 기준으로 내림차순으로 되었습니다.

API는 아래 링크를 통해 조회 가능합니다.
* 전체 이벤트 : https://irunseoul-3204d.firebaseio.com/event.json
* 년간 이벤트 : https://irunseoul-3204d.firebaseio.com/event/2017.json


##### Response Values

| Name               | Type | Definition |
|--------------------|------|------------|
| application_period |      |            |
| city               |      |            |
| date               |      |            |
| description        |      |            |
| email              |      |            |
| host               |      |            |
| latitude           |      |            |
| location           |      |            |
| longitude          |      |            |
| map_url            |      |            |
| phone              |      |            |
| race               |      |            |
| temperature        |      |            |
| title              |      |            |
| weather            |      |            |
| website            |      |            |

```json
{"application_period":"2016/12/12 - 2017/2/28","city":"지역","date":"2017/03/19 08:00",
"description":"서울국제마라톤 겸 제88회 동아마라톤","email":"marathon@donga.com","host":"동아일보사","latitude":"37.5726574782299","location":"서울광화문광장, 올림픽공원, 잠실주경기장","longitude":"126.97692131590603","map_url":"http://map.daum.net/link/map/8193961",
"phone":"02-361-1425","race":["풀","10km","2인릴레이","4인릴레이"],
"temperature":"","title":"서울국제마라톤 겸 제88회 동아마라톤",
"weather":"21","website":"http://www.seoul-marathon.com"}
```

## Python3 Packages
* beautifulSoup, requests, forecastio

## Developement Setup

1. Go to your working directory and install Python virtual environment

```
python3 -m venv marathonvenv
```

2. Activate Python virtual environment 
```
source marathonvenv/bin/activate
```
3. Install Python Packages
```
pip3 install requests python-forecastio beautifulsoup4
```

# TODO 
firebase API Integration

