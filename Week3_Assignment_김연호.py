import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient as mc

#서버 셋팅
client = mc('localhost', 27017)
db = client.genie_music

#User Agnet 입력
headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

# 2019.09.29일 1윌부터 200위 까지 Data 추출
for page in range(1,5):
    #크롤링 초기 셋팅
    address = 'https://www.genie.co.kr/chart/top200?ditc=D&ymd=20190929&hh=10&rtm=N&pg={}'.format(page)
    data = requests.get(address, headers=headers)
    soup = bs(data.text, 'html.parser')
    music_rank = soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr.list > td.number')
    music_info = soup.select('#body-content > div.newest-list > div.music-list-wrap > table.list-wrap > tbody > tr.list > td.info > a')
    #카테고리별 리스트
    rank_list = []
    info_list = []
    title_list = []
    singer_list = []
    album_list = []
    doc_dic = {}

    for number in music_rank:
        rank_list.append(number.text.replace('\n', '')[0:3:1])

    for info in music_info:
        info_list.append(info.text.replace('\n','').replace(' ',''))
    title_list = info_list[::3]
    singer_list = info_list[1::3]
    album_list = info_list[2::3]
    for i in range(len(rank_list)):
        doc_dic = {'rank':rank_list[i], 'title':title_list[i],'singer':singer_list[i], 'album':album_list[i]}
        db.genie_music.insert_one(doc_dic)
