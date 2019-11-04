import pprint
import json
import requests
import os
import time
import re
import random
from datetime import datetime

from newsapi import NewsApiClient
from django.shortcuts import render
from django.http import JsonResponse
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
from .models import Schedule, Main_test, Ranked_cut, Care, stretch

nugu_host = "블랑"

# Create your views here.
customer_name = '블랑'

subject_time_dict = {
    '국어' : 80, '수학' : 100, '영어' : 70, '과탐' : 30, '사탐' : 30, '한국사' : 30
}

day_list = {1 : 31, 2 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}

# grade_num = 0
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


# 과목 시험 시간 받기(알람 기능 지원 불가. 포기)
def check_schedule(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    
    pprint.pprint(nugu_body)
    
    if nugu_body.get('action').get('parameters').get('dt_day'):
        nugu_subject = nugu_body.get('action').get('dt_day').get('subject').get('value')
        
        
        subject_time = subject_time_dict[nugu_subject]
    
    if nugu_body.get('action').get('parameters').get('subject'):
        nugu_subject = nugu_body.get('action').get('parameters').get('subject').get('value')
        subject_time = subject_time_dict[nugu_subject]
    
    # #     # 2. 응답 만들기
    # # 필수 : output, resultCode
    # result = nugu_body
    # result['output'] = {'test_time': subject_time }
    # result['resultCode'] = 'OK'
    # pprint.pprint(result)
    
    return JsonResponse(result)


# 국어 점수만 받기 초안
def year_ko_ab(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    if nugu_body.get('action').get('parameters').get('year_name'):
        year = int(nugu_body.get('action').get('parameters').get('year_name').get('value'))
        tmp = Main_test.objects.filter(year=year)[0]
        print(tmp)
        seq = tmp.seq
    if nugu_body.get('action').get('parameters').get('subject_name'):
        subject = nugu_body.get('action').get('parameters').get('subject_name').get('value')
        if nugu_body.get('action').get('parameters').get('a_b'):
            subject += nugu_body.get('action').get('parameters').get('a_b').get('value')
        sub_cod = sub_code[subject]
    
    print(year)
    print(seq)
    print(sub_cod)

    
    if year < 14:
        url = f'http://www.megastudy.net/Entinfo/pda/User_Ans_Anal.asp?seq={seq}&sub_cod={sub_cod}&years={year}'
        
    else:
        url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_type=&sub_cod={sub_cod}"
        
    print(url)
  
    
# 답안 크롤링 초안
def index(request):
    
    year = 2006
    seq = 29
    tab_num = 2
    sub_cod = 2101
    
    if year < 14:
        url = f'http://www.megastudy.net/Entinfo/pda/User_Ans_Anal.asp?seq={seq}&sub_cod={sub_cod}&years={year}'
        
    else:
        url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_type=&sub_cod={sub_cod}"
    # print(url)
    # http://www.megastudy.net/Entinfo/pda/detail_list3_new_2016.asp?seq=213&exam_type=&tab_no=2&sub_cod=2005
    
    response = requests.get(url)
    # html = response.text
    html = urlopen(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    # soup = soup.prettify()
    # print(soup)
    # print(type(soup))
    html = list(soup.children)[4]
    answers = html.find('table').get_text()
    # print(type(answers))
    listen = list(answers.split())
    # print(listen)
    cnt = 0
    for i in range(len(listen)):
        if listen[i]=='5' and listen[i-1]=='4' and listen[i-2]=='3' and listen[i-3]=='2' and listen[i-4]=='1':
            # print(listen[i+1],listen[i+1])
            start = i+1
            break
    
    if tab_num==2:
        while True:
            if '정답률은' in listen[start : start + 7]:
                break
            if listen[start+6]=='(주관식)':
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                start += 7
            else:
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                start += 10
    else:
        while True:
            if '정답률은' in listen[start : start + 7]:
                break
            print('{}번에 {}'.format(listen[start], listen[start + 1]))
            start += 10
            
    

    return render(request, 'index.html', {'soup' : soup.prettify(), 'html':html, 'answers' : answers, 'listen':listen}) 
    
# 입시정보 > 아니
def infom_other_information(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')
    
    query = urllib.parse.quote('수능')
    url = "https://openapi.naver.com/v1/search/news.json?query=" + query
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    response = urlopen(req)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
    else:
        response_body = 'None'
    response = json.loads(response_body)
    response_text = response['items'][0]['title']
    response_text = re.sub('<.+?>', '', response_text, 0).strip()
    response_text = re.sub('&quot;', '', response_text)
    
    result = nugu_body
    result['output'] = {'news_information': response_text}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    return JsonResponse(result)
# 입시정보 > 네
def inform_univ_information(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    result = nugu_body
    result['output'] = {'name_1': customer_name}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    return JsonResponse(result)
# 입시정보 > 네 > 네
def inform_univ_my(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')
    
    target_univ = Ranked_cut.objects.get(pk=1).college
    target_query = target_univ + ' 입시'
    query = urllib.parse.quote(target_query)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + query
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    response = urlopen(req)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
    else:
        response_body = 'None'
    response = json.loads(response_body)
    response_text = response['items'][0]['title']
    response_text = re.sub('<.+?>', '', response_text, 0).strip()
    response_text = re.sub('&quot;', '', response_text)
    
    result = nugu_body
    result['output'] = {'name_1': customer_name, 'univ_1': target_univ, 'information_myuniv': response_text}
    result['resultCode'] = 'OK'
    # pprint.pprint(result)
    return JsonResponse(result)
# 입시정보 > 네 > 아니 > 대학입력
def answer_univ_other(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    client_id = os.getenv('NAVER_CLIENT_ID')
    client_secret = os.getenv('NAVER_CLIENT_SECRET')
    pprint.pprint(nugu_body)
    nugu_univ_name = nugu_body.get('action').get('parameters').get('univ_name').get('value')
    nugu_univ_query = nugu_univ_name + ' 입시'
    query = urllib.parse.quote(nugu_univ_query)
    url = "https://openapi.naver.com/v1/search/news.json?query=" + query
    req = urllib.request.Request(url)
    req.add_header("X-Naver-Client-Id", client_id)
    req.add_header("X-Naver-Client-Secret", client_secret)
    response = urlopen(req)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
    else:
        response_body = 'None'
    response = json.loads(response_body)
    response_text = response['items'][0]['title']
    response_text = re.sub('<.+?>', '', response_text, 0).strip()
    response_text = re.sub('&quot;', '', response_text)
    result = nugu_body
    result['output'] = {'name_1': customer_name, 'univ_name': nugu_univ_name, 'information_univ': response_text}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)

# 스케쥴 있는지 질문.
def ask_read(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    doing_list = []
    
    inform_0 = ""
    if nugu_body.get('action').get('parameters').get('day_0'):
        dt_day = nugu_body.get('action').get('parameters').get('day_0').get('value')
        if dt_day == 'TODAY':
            dt = datetime.now()
            dt_month = dt.month
            dt_day = dt.day
            schedules = Schedule.objects.filter(month = dt_month).filter(day = dt_day)
            print(schedules)

            if schedules:
                for i in schedules:
                    doing_list.append([i.start_time, i.name])
            
        else:
            dt_month, dt_day = dt_day.split()
            dt_month = int(dt_month[:-1])
            dt_day = int(dt_day[:-1])
            schedules = Schedule.objects.filter(month = dt_month).filter(day = dt_day)
            print(schedules)

            if schedules:
                for i in schedules:
                    doing_list.append([i.start_time, i.name])
    
    
    
    if not doing_list:
        inform_0 = ' 없으시네요'
        print(inform_0)
    else:
        doing_list.sort()
        for j in doing_list:
            inform_0 += f"{j[0]}시에 {j[1]} "
        inform_0 += "입니다."
        print(inform_0)
    
    
            
    result = nugu_body
    
    pprint.pprint(result)
    
    result['output'] = {'inform_0' : inform_0}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
        
    return JsonResponse(result)

# 스케쥴 추가
def schedule_upgrade_content(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    schedule = Schedule()
    schedule.check = False
    
    if nugu_body.get('action').get('parameters').get('day_1'):
        dt_day = nugu_body.get('action').get('parameters').get('day_1').get('value')
        if dt_day == 'TODAY':
            dt = datetime.now()
            dt_month = dt.month
            dt_day = dt.day
            
        else:
            dt_month, dt_day = dt_day.split()
            dt_month = int(dt_month[:-1])
            dt_day = int(dt_day[:-1])
            
            
    if dt_month <= 12 and dt_month > 0:
        schedule.month = dt_month
    else:
        inform_1 += "올바른 달을 말씀해주세요."
        
        
        
    if dt_day > 0 and dt_day <= day_list[dt_month]:
        schedule.day = dt_day
    else:
        inform_1 += "올바른 일을 말씀해주세요."
        
        
        
        
    if nugu_body.get('action').get('parameters').get('time_1'):
        dt_time = int(nugu_body.get('action').get('parameters').get('time_1').get('value'))
        schedule.start_time = dt_time
         
    content = ""
    
    if nugu_body.get('action').get('parameters').get('content_1_0'):
        content += nugu_body.get('action').get('parameters').get('content_1_0').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_1_1'):
        content += nugu_body.get('action').get('parameters').get('content_1_1').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_1_2'):
        content += nugu_body.get('action').get('parameters').get('content_1_2').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_1_3'):
        content += nugu_body.get('action').get('parameters').get('content_1_3').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_1_4'):
        content += nugu_body.get('action').get('parameters').get('content_1_4').get('value') + ' '
    
    schedule.name = content

    
    inform_1 = ""


    if dt_time <= 24 and dt_time > 0:
        schedule.start_time = dt_time
    else:
        inform_1 += "올바른 시간을 말씀해주세요."
        
    
    
    if not inform_1:
        schedule.save()
        inform_1 = f"{dt_month}월 {dt_day}일 {content}로 저장되었습니다."
        
        
    result = nugu_body
    
    pprint.pprint(result)
    
    result['output'] = {'inform_1' : inform_1}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
        
    return JsonResponse(result)
    
# 스케쥴 수정
def edit_content(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)

    # 월/일 입력
    if nugu_body.get('action').get('parameters').get('day_2'):
        dt_day = nugu_body.get('action').get('parameters').get('day_2').get('value')
        if dt_day == 'TODAY':
            dt = datetime.now()
            dt_month = dt.month
            dt_day = dt.day
            
        else:
            dt_month, dt_day = dt_day.split()
            dt_month = int(dt_month[:-1])
            dt_day = int(dt_day[:-1])
            
      
    # 시간 입력
    if nugu_body.get('action').get('parameters').get('time_2'):
        dt_time = int(nugu_body.get('action').get('parameters').get('time_2').get('value'))
        
    
    # 내용 입력
    content = ""
    
    if nugu_body.get('action').get('parameters').get('content_2_0'):
        content += nugu_body.get('action').get('parameters').get('content_2_0').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_2_1'):
        content += nugu_body.get('action').get('parameters').get('content_2_1').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_2_2'):
        content += nugu_body.get('action').get('parameters').get('content_2_2').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_2_3'):
        content += nugu_body.get('action').get('parameters').get('content_2_3').get('value') + ' '
    if nugu_body.get('action').get('parameters').get('content_2_4'):
        content += nugu_body.get('action').get('parameters').get('content_2_4').get('value') + ' '
    
    
    if dt_month and dt_day and dt_time and content:
        schedule = Schedule.objects.filter(month = dt_month).filter(day = dt_day).filter(start_time = dt_time)[0]
    
    
        
    inform_2 = ""
    if dt_month <= 12 and dt_month > 0:
        schedule.month = dt_month
    else:
        inform_2 += "올바른 달을 말씀해주세요."
        
    if dt_day > 0 and dt_day <= day_list[dt_month]:
        schedule.day = dt_day
    else:
        inform_2 += "올바른 일을 말씀해주세요."
        
    if dt_time <= 24 and dt_time > 0:
        schedule.start_time = dt_time
    else:
        inform_2 += "올바른 시간을 말씀해주세요."   
    
    schedule.name = content


    
    if not inform_2:
        schedule.save()
        inform_2 = f"{dt_month}월 {dt_day}일 {content}로 수정되었습니다."
    
    result = nugu_body
    
    pprint.pprint(result)
    
    result['output'] = {'inform_2' : inform_2}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
        
    return JsonResponse(result)


# 스케쥴 삭제
def delete_finish(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    
    inform_3 = ""
    
    if nugu_body.get('action').get('parameters').get('day_3'):
        dt_day = nugu_body.get('action').get('parameters').get('day_3').get('value')
        if dt_day == 'TODAY':
            dt = datetime.now()
            dt_month = dt.month
            dt_day = dt.day
            
        else:
            dt_month, dt_day = dt_day.split()
            dt_month = int(dt_month[:-1])
            dt_day = int(dt_day[:-1])
            
    
    if nugu_body.get('action').get('parameters').get('time_3'):
        dt_time = int(nugu_body.get('action').get('parameters').get('time_3').get('value'))
    
    schedule = Schedule.objects.filter(month = dt_month).filter(day = dt_day).filter(start_time = dt_time)[0]
    

    if dt_month <= 12 and dt_month > 0:
        schedule.month = dt_month
    else:
        inform_3 += "올바른 달을 말씀해주세요."
        
    if dt_day > 0 and dt_day <= day_list[dt_month]:
        schedule.day = dt_day
    else:
        inform_3 += "올바른 일을 말씀해주세요."
    
    if dt_time <= 24 and dt_time > 0:
        schedule.start_time = dt_time
    else:
        inform_3 += "올바른 시간을 말씀해주세요."

    if not inform_3:
        schedule.delete()
        inform_3 = "삭제되었습니다."

    result = nugu_body
    
    pprint.pprint(result)
    
    result['output'] = {'inform_3' : inform_3}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
        
    return JsonResponse(result)
    

def shrkek(subject):
    if subject=='국어' or subject=='국어A' or subject=='국어B' or subject=='언어':
        # table_no = 1
        return 1
        
    elif subject=='수학가' or subject=='수학나' or subject=='수학A' or subject=='수학B' or subject=='수리가' or subject=='수리나' or subject=='미분과적분' or subject=='확률과통계' or subject=='이산수학':
        # table_no = 2
        return 2
        
    elif subject=='영어' or subject=='영어A' or subject=='영어B' or subject=='외국어':
        # table_no = 3
        return 3
        
    elif subject=='한국사' or subject=='생활과윤리' or subject=='윤리와사상' or subject=='한국지리' or subject=='세계지리' or subject=='동아시아사' or subject=='세계사' or subject=='법과정치' or subject=='경제' or subject=='사회문화' or subject=='윤리' or subject=='경제지리' or subject=='국사' or subject=='한국근현대사' or subject=='법과사회' or subject=='정치':
        # table_no = 4
        return 4
    elif subject=='물리1' or subject=='물리2' or subject=='화학1' or subject=='화학2' or subject=='생명과학1' or subject=='생명과학2' or subject=='지구과학1' or subject=='지구과학2' or subject=='생물1' or subject=='생물2':
        # table_no = 5
        return 5
        
    elif subject=='한문' or subject=='독일어' or subject=='프랑스어' or subject=='스페인어' or subject=='중국어' or subject=='일본어' or subject=='러시아어' or subject=='아랍어' or subject=='기초베트남어':
        # table_no = 6
        return 6


# 수능. 수학 제외 답안 가져오기
def answer_subject_num(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)


    # # nugu에게 받는것: title, grade, year, subject, subject_num
    # #                  제목   학년   년도   과목     유형있는지
    if nugu_body.get('action').get('parameters').get('title'):
        title = nugu_body.get('action').get('parameters').get('title').get('value')
    
    if nugu_body.get('action').get('parameters').get('grade'):
        grade = nugu_body.get('action').get('parameters').get('grade').get('value')
    
    if nugu_body.get('action').get('parameters').get('year'):
        year = nugu_body.get('action').get('parameters').get('year').get('value')
        year = int(year)
        tmp = Main_test.objects.filter(year=year)[0]
        print(tmp)
        seq = tmp.seq
    
    if nugu_body.get('action').get('parameters').get('subject'):
        subject = nugu_body.get('action').get('parameters').get('subject').get('value')
        tab_no = shrkek(subject) #과목입력받으면 table_no를 받는다.
    
    if nugu_body.get('action').get('parameters').get('subject_num'):
        subject_num = nugu_body.get('action').get('parameters').get('subject_num').get('value')
        subject += subject_num
    
    sub_cod = sub_code[subject] # 서브코드, 가or나, 과탐사탐 항목들
    
    if nugu_body.get('action').get('parameters').get('subject_num'):
        subject_num = nugu_body.get('action').get('parameters').get('subject_num').get('value')
    #=========================================================================================#
    
    
    #=========================================================================================#
    print(year)
    print(title)
    print(subject_num)

    
    
    # year = 2019
    # seq = 247
    # subject = "수학나"
    
    tab_num = shrkek(subject)
    sub_cod = sub_code[subject]
    
    if year < 14:
        url = f'http://www.megastudy.net/Entinfo/pda/User_Ans_Anal.asp?seq={seq}&sub_cod={sub_cod}&years={year}'
        
    else:
        # url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_type=&sub_cod={sub_cod}"
        if tab_num == 2 or tab_num == 5 or tab_num == 6: #수학,과탐,사탐은 서브코드를 받아야한다
            url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_grd=3&years={year}&tab_no={tab_num}&sub_cod={sub_cod}"
        else:
            url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_grd=3&years={year}&tab_no={tab_num}"
        
    print(url)
    
    response = requests.get(url)
    # html = response.text
    html = urlopen(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    # soup = soup.prettify()
    # print(soup)
    # print(type(soup))
    
    
    
    
    html = list(soup.children)[4]
    answers = html.find('table').get_text()
    # print(type(answers))
    listen = list(answers.split())
    # print(listen)
    cnt = 0
    
    for i in range(len(listen)):
        if listen[i]=='5' and listen[i-1]=='4' and listen[i-2]=='3' and listen[i-3]=='2' and listen[i-4]=='1':
            # print(listen[i+1],listen[i+1])
            start = i+1
            break
    
    answer = ""
    
    cnt = 0
    if tab_num==2:
        while True:
            cnt += 1
            if '정답률은' in listen[start : start + 7]:
                break
            if listen[start+6]=='(주관식)':
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                answer += f'{listen[start]}번에 {listen[start + 1]}, '
                start += 7
            else:
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                answer += f'{listen[start]}번에 {listen[start + 1]}, '
                start += 10
                
            
            if not cnt % 5:
                answer += "."
    else:
        while True:
            cnt += 1
            if '정답률은' in listen[start : start + 7]:
                break
            print('{}번에 {}'.format(listen[start], listen[start + 1]))
            answer += f'{listen[start]}번에 {listen[start + 1]}, '
            start += 10
            
            if not cnt % 5:
                answer += "."
    
    answer_5 = answer
    
    
    
    
    
    #====================================================================================#
    result = nugu_body
    result['output'] = {'answer_5': answer_5 }
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)
    #====================================================================================#

    # return render(request, 'test2.html', {'soup' : soup.prettify(), 'html':html, 'answers' : answers, 'listen':listen, 'answer':answer}) 

# 수능. 수학 제외 답안. 유형 없을 때
def check_no_num(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)


    # # nugu에게 받는것: title, grade, year, subject, subject_num
    # #                  제목   학년   년도   과목     유형있는지
    if nugu_body.get('action').get('parameters').get('title'):
        title = nugu_body.get('action').get('parameters').get('title').get('value')
    
    if nugu_body.get('action').get('parameters').get('grade'):
        grade = nugu_body.get('action').get('parameters').get('grade').get('value')
    
    if nugu_body.get('action').get('parameters').get('year'):
        year = nugu_body.get('action').get('parameters').get('year').get('value')
        year = int(year)
        tmp = Main_test.objects.filter(year=year)[0]
        print(tmp)
        seq = tmp.seq
    
    if nugu_body.get('action').get('parameters').get('subject'):
        subject = nugu_body.get('action').get('parameters').get('subject').get('value')
        tab_no = shrkek(subject) #과목입력받으면 table_no를 받는다.
    
    
    #=========================================================================================#
    print(year)
    print(title)
    print(subject)

    
    
    # year = 2019
    # seq = 247
    # subject = "수학나"
    
    tab_num = shrkek(subject)
    sub_cod = sub_code[subject]
    
    if year < 14:
        url = f'http://www.megastudy.net/Entinfo/pda/User_Ans_Anal.asp?seq={seq}&sub_cod={sub_cod}&years={year}'
        
    else:
        # url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_type=&sub_cod={sub_cod}"
        if tab_num == 2 or tab_num == 5 or tab_num == 6: #수학,과탐,사탐은 서브코드를 받아야한다
            url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_grd=3&years={year}&tab_no={tab_num}&sub_cod={sub_cod}"
        else:
            url = f"http://www.megastudy.net/Entinfo/pda/detail_list3_new.asp?seq={seq}&exam_grd=3&years={year}&tab_no={tab_num}"
        
    print(url)
    
    response = requests.get(url)
    # html = response.text
    html = urlopen(url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    soup = BeautifulSoup(html, 'html.parser')
    # soup = soup.prettify()
    # print(soup)
    # print(type(soup))
    
    
    
    
    html = list(soup.children)[4]
    answers = html.find('table').get_text()
    # print(type(answers))
    listen = list(answers.split())
    # print(listen)
    cnt = 0
    
    for i in range(len(listen)):
        if listen[i]=='5' and listen[i-1]=='4' and listen[i-2]=='3' and listen[i-3]=='2' and listen[i-4]=='1':
            # print(listen[i+1],listen[i+1])
            start = i+1
            break
    
    answer = ""
    
    cnt = 0
    if tab_num==2:
        while True:
            cnt += 1
            if '정답률은' in listen[start : start + 7]:
                break
            if listen[start+6]=='(주관식)':
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                answer += f'{listen[start]}번에 {listen[start + 1]}, '
                start += 7
            else:
                print('{}번에 {}'.format(listen[start], listen[start + 1]))
                answer += f'{listen[start]}번에 {listen[start + 1]}, '
                start += 10
                
            
            if not cnt % 5:
                answer += "."
    else:
        while True:
            cnt += 1
            if '정답률은' in listen[start : start + 7]:
                break
            print('{}번에 {}'.format(listen[start], listen[start + 1]))
            answer += f'{listen[start]}번에 {listen[start + 1]}, '
            start += 10
            
            if not cnt % 5:
                answer += "."
    
    answer_4 = answer
    
    
    
    
    
    #====================================================================================#
    result = nugu_body
    result['output'] = {'answer_4': answer_4 }
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)
    #====================================================================================#

    # return render(request, 'test2.html', {'soup' : soup.prettify(), 'html':html, 'answers' : answers, 'listen':listen, 'answer':answer}) 
    
      

# 등급 읽을 수 있는지 확인용.
'''
def answer_grade_result(request):
    global grade_num
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    
    if nugu_body.get('action').get('parameters').get('grade_num'):
        grade_num_tmp = nugu_body.get('action').get('parameters').get('grade_num').get('value')
    grade_num =float(grade_num_tmp)
    
    # print(grade_num)
    # col = univ_list.college
    
    # for i in univ_list:
    #     print(i.college)
    
    return render(request,'test1.html',{'grade_num':grade_num,"univ_list":univ_list})
'''


# 정하지 않은 대학교에 등급 비교
def compare_with_other(request):
    # global grade_num
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    
    if nugu_body.get('action').get('parameters').get('grade_num'):
        grade_num = nugu_body.get('action').get('parameters').get('grade_num').get('value')
    
    aa = float(grade_num) - 1.0
    bb = float(grade_num) + 1.0
    univ_list = Ranked_cut.objects.filter(grade_cut__gt=aa, grade_cut__lt=bb)# gt = greater than, lt = less than
    
    univ_other = ""
    for univ in univ_list:
        print(univ)
        univ_other += univ.college + ", "
    print(univ_other)
    # return render(request,'test1.html',{'grade_num':grade_num,"univ_other":univ_other})
    result = nugu_body
    result['output'] = {'univ_other': univ_other }
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)


# 저장해놓은 대학교 등급 비교 (sk대학교)
def compare_with_goal(request):
    global grade_num
    nugu_body = json.loads(request.body, encoding='utf-8')
    pprint.pprint(nugu_body)
    # 받은 grade_num과 비교하여 안정권인 대학 string 을 누구에게 보내준다.
    # grade_num = 2.0
    
    tmp_inform = ""
    
    if nugu_body.get('action').get('parameters').get('grade_num'):
        my_score = float(nugu_body.get('action').get('parameters').get('grade_num').get('value'))
    
    goal_score = float(Ranked_cut.objects.filter(college = '서울대학교')[0].grade_cut)
    
    if int(my_score) == int(goal_score):
        tmp_inform = "안정권이에요."
    else:
        tmp_inform = "조금 더 분발하셔야겠어요."
    
    univ = f"서울대학교의 등급컷은 {goal_score}. {nugu_host}님의 평균 등급은 {my_score}로, " + tmp_inform
    

    result = nugu_body
    result['output'] = {'univ': univ }
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)
    # return render(request,'test2.html',{"compare_univ":compare_univ,"univ":univ})

# 건강관리
def health(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    if nugu_body.get('action').get('parameters').get('condition'):
        condition = nugu_body.get('action').get('parameters').get('condition').get('value')
        print(condition)
    if condition == '불면증':
        print(condition)
        response_text = Care.objects.filter(symptom=condition)
        response_text = random.choice(response_text).food
        response_text += '입니다. 불면증에 관련된 스트레칭 알려드릴까요?'
    elif condition == '스트레스':
        response_text = Care.objects.filter(symptom=condition)
        response_text = random.choice(response_text).food
        response_text += '입니다. 스트레스에 관련된 스트레칭 알려드릴까요?'
    elif condition == '집중력':
        response_text = Care.objects.filter(symptom=condition)
        response_text = random.choice(response_text).food
        response_text += '입니다. 스트레스에 관련된 스트레칭 알려드릴까요?'
    elif condition == '몸살':
        response_text = Care.objects.filter(symptom=condition)
        response_text = random.choice(response_text).food
        response_text += '입니다.'
    
    result = nugu_body
    result['output'] = {'condition_answer': response_text, 'condition': condition}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)

# 불면증 스트레칭
def condition_insomnia(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    condition = '불면증'
    response_text = stretch.objects.filter(symptom=condition)
    response_text = random.choice(response_text).action
    
    result = nugu_body
    result['output'] = {'insomnia_stretching': response_text, 'condition': condition}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)
    
# 스트레스 스트레칭
def condition_stress(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    condition = '스트레스'
    response_text = stretch.objects.filter(symptom=condition)
    response_text = random.choice(response_text).action
    
    result = nugu_body
    result['output'] = {'stress_stretching': response_text, 'condition': condition}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)
    
# 집중력 스트레칭
def condition_concentration(request):
    nugu_body = json.loads(request.body, encoding='utf-8')
    condition = '집중력'
    response_text = stretch.objects.filter(symptom=condition)
    response_text = random.choice(response_text).action
    
    result = nugu_body
    result['output'] = {'concentration_stretching': response_text, 'condition': condition}
    result['resultCode'] = 'OK'
    pprint.pprint(result)
    return JsonResponse(result)