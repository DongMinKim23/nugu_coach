import pprint
import json
import requests
import os
import time

from newsapi import NewsApiClient
from django.shortcuts import render
from django.http import JsonResponse
from urllib.request import urlopen
from bs4 import BeautifulSoup

# Create your views here.
google_api_key = '4f6ea9267c944722a1f49b16bdb4d43a'

subject_time_dict = {
    '국어' : 80, '수학' : 100, '영어' : 70, '과탐' : 30, '사탐' : 30, '한국사' : 30
}

sub_code = {
    '국어' : 1003, '국어A' : 1001, '국어B' : 1002, '언어' : 1000,
    '수학가' : 2004, '수학나' : 2005, '수학A' : 2001, '수학B' : 2002,
    '수리가' : 2101, '수리나' : 2200, '미분과적분' : 2101, '확률과 통계' : 2102,
    '이산수학' : 2103, '영어' : 3003, '영어A' : 3001, '영어B' : 3002, 
    '외국어' : 3000, '한국사' : 4113, '생활과윤리' : 4117, '윤리와사상' : 4118, 
    '한국지리' : 4102, '세계지리' : 4103, '동아시아사' : 4116, '세계사' : 4107,
    '법과정치' : 4119, '경제' : 4110, '사회문화' : 4111, '윤리' : 4101, '경제지리' : 4104,
    '경제' : 4110, '사회문화' : 4111, '윤리' : 4101, '경제지리' : 4104, '국사' : 4105,
    '한국근현대사' : 4106, '법과사회' : 4108, '정치' : 4109, '경제' : 4110,
    '물리1' : 4201, '물리2' : 4202, '화학1' : 4203, '화학2' : 4204, '생명과학1' : 4213,
    '생명과학2' : 4214, '지구과학1' : 4207, '지구과학2' : 4208, '생물1' : 4205, '생물2' : 4206,
    '한문' : 5001, '독일어' : 5002, '프랑스어' : 5003, '스페인어' : 5004, '중국어' : 5005,
    '일본어' : 5006, '러시아어' : 5007, '아랍어' : 5008, '기초베트남어' : 5009
    
}



def check_schedule(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    
    pprint.pprint(nugu_body)
    
    if nugu_body.get('action').get('parameters').get('dt_day'):
        nugu_subject = nugu_body.get('action').get('dt_day').get('subject').get('value')
        
        
        subject_time = subject_time_dict[nugu_subject]
    
    # if nugu_body.get('action').get('parameters').get('subject'):
    #     nugu_subject = nugu_body.get('action').get('parameters').get('subject').get('value')
    #     subject_time = subject_time_dict[nugu_subject]
    
    # #     # 2. 응답 만들기
    # # 필수 : output, resultCode
    # result = nugu_body
    # result['output'] = {'test_time': subject_time }
    # result['resultCode'] = 'OK'
    # pprint.pprint(result)
    
    return JsonResponse(result)

# def subject(request):


def index(request):
    year = 
    seq = 213
    tab_num = 2
    sub_code = 2005
    if year < 14:
        url = f'http://www.megastudy.net/Entinfo/pda/User_Ans_Anal.asp?seq={seq}&sub_cod={sub_cod}&years={year}'
    else:
        url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_type=&tab_no={tab_num}&sub_cod={sub_cod}"
    # http://www.megastudy.net/Entinfo/pda/detail_list3_new_2016.asp?seq=213&exam_type=&tab_no=2&sub_cod=2005

    
    
    
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(response.text, 'html.parser')
    # soup = soup.prettify()
    # print(soup)
    print(type(soup))
    # table = soup.find_all("table")
    # table = table.find_all("table")
    # table = table.select("table")
    # table = soup.select("#wrap_2014 > div.column_main > div.column_right > table > tbody > tr > td > table")
    # table = soup.select("#iContent_list")
    # print(table)
    # print(table.text)
    # print(table.text)
    
    # print(bsObject.body)
    
    # for table in bsObject.find_all('table'):
    #     pprint.pprint(table)
    # return JsonResponse({})
    # return render(request, 'index.html', {'soup' : soup.prettify(),'table' : table}) 
    return render(request, 'index.html', {'soup' : soup.prettify(), 'html':html}) 
    

def news(request):
    # Documents: https://newsapi.org/docs/endpoints/top-headlines
    # Python Example: https://newsapi.org/docs/client-libraries/python
    # 크롤링을 위한 인스턴스 선언
    newsapi = NewsApiClient(api_key=google_api_key)
    # news : 제목과 기사 포함한 전체내용
    news = newsapi.get_everything(q='수능')
    # headlines : 제목만, 근데 
    headlines = newsapi.get_top_headlines(q='수능', country='kr')
    context = { 'news': news, 'headlines': headlines }
    query = '수능'
    # 다른 형태로 변경
    baseurl = 'https://newsapi.org/v2/top-headlines?country=kr&apiKey=%s&q=%s' % (google_api_key, query)
    print(query)
    return render(request, 'news.html', context)
    
    
def edit_schedule(request):
    
    nugu_body = json.loads(request.body, encoding='utf-8')
    
    pprint.pprint(nugu_body)
    
    if nugu_body.get('action').get('parameters').get('subject'):
        nugu_subject = nugu_body.get('action').get('parameters').get('subject').get('value')
        subject_time = subject_time_dict[nugu_subject]
    
    #     # 2. 응답 만들기
    # 필수 : output, resultCode
    result = nugu_body
    result['output'] = {'test_time': subject_time }
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    
    return JsonResponse(result)






def shrkek():
    if subject=='국어' or subject=='국어A' or subject=='국어B' or subject=='언어':
        table_no = 1
    elif subject=='수학가' or subject=='수학나' or subject=='수학A' or subject=='수학B' or subject=='수리가' or subject=='수리나' or subject=='미분과적분' or subject=='확률과통계' or subject=='이산수학':
        table_no = 2
    elif subject=='영어' or subject=='영어A' or subject=='영어B' or subject=='외국어':
        table_no = 3
    elif subject=='한국사' or subject=='생활과윤리' or subject=='윤리와사상' or subject=='한국지리' or subject=='세계지리' or subject=='동아시아사' or subject=='세계사' or subject=='법과정치' or subject=='경제' or subject=='사회문화' or subject=='윤리' or subject=='경제지리' or subject=='국사' or subject=='한국근현대사' or subject=='법과사회' or subject=='정치':
        table_no = 4
    elif subject=='물리1' or subject=='물리2' or subject=='화학1' or subject=='화학2' or subject=='생명과학1' or subject=='생명과학2' or subject=='지구과학1' or subject=='지구과학2' or subject=='생물1' or subject=='생물2':
        table_no = 5
    elif subject=='한문' or subject=='독일어' or subject=='프랑스어' or subject=='스페인어' or subject=='중국어' or subject=='일본어' or subject=='러시아어' or subject=='아랍어' or subject=='기초베트남어':
        table_no = 6