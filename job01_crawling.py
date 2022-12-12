#자연어기반 오디오 소설 추천시스템
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

#크롤링코드 만든다음에 크롤링 분담하여
options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)          # 드라이버

url = 'https://audioclip.naver.com/audiobook-categories/3/audiobooks'     # 페이지


# <x_path 원본 모음>
# 0. 제목버튼                //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a/div[2]   => title_button_xpath  # 제목눌러서 상세로 들어가기
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a/div[2]/div[2] 추천
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[2]/a/div[2]/div[1]
#                       //*[@id="content"]/div/section/div/div/div[3]/div/div/div[3]/a/div[2]/div[2] 요약
# => 0. 링크클릭          //*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a

# 1. 상세>제목             //*[@id="content"]/div/section/div[1]/div[2]/h3                          => title_xpath
# 2. 상세>저자             //*[@id="content"]/div/section/div[1]/div[3]/div[1]/span[1]/text()[1]    => author_xpath
# 3. 상세>오디오북 정보     //*[@id="audiobook"]/div[1]/p      #/text()                              => inform_xpath



title_click_xpath = '//*[@id="content"]/div/section/div/div/div[3]/div/div/div[1]/a'                    # 0. (제목)버튼  # 상세페이지로 가기위한
title_xpath = '//*[@id="content"]/div/section/div[1]/div[2]/h3'                                         # 1. 상세>제목
author_xpath = '//*[@id="content"]/div/section/div[1]/div[3]/div[1]/span[1]/text()[1]'                  # 2. 상세>저자
inform_xpath = '//*[@id="audiobook"]/div[1]/p'                                                          # 3. 상세>오디오북 정보









# your_clip = 2018              # 각자의 클립 할당량
# for page in range(33, 51):    # (1~31) 페이지 = i  # i 값으로 페이지 접근할 것이니 몇 까지 있는지 확인
#     url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_clip, page) # 페이지
#     titles = []           # 받아올 것 1 = 영화 20개 긁어을 때마다 저장합시다, 여기다 어펜드 시켜야하는
#     reviews = []          # 받아올 것 2 = 영화 20개 긁어을 때마다 저장합시다, 여기다 어펜드 시켜야하는
#     try:
#
#         for title_num in range(1, 21):                  # 제목 j   # X_path 따기 20개씩 있으니 for문 20개씩 돌아야.
#             driver.get(url)                     # 드라이버 겟 여기서 하니까 계속 다시함 (새로고침)
#             time.sleep(0.1)                     # 열고 잠시 기다려주고
#
#             movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)    # 제목
#
#             title = driver.find_element('xpath', movie_title_xpath).text    # 텍스트만 가져오면 됨
#
#             print('title', title)
#             driver.find_element('xpath', movie_title_xpath).click()  # 클릭
#             time.sleep(0.1)
#             # print(title)
#             # print('debug01')
#
#             try:    # 리뷰 누르다가 에러나는 것이니
#                 driver.find_element('xpath', review_button_xpath).click()      # 클릭
#                 time.sleep(0.1)
#
#                 review_num = driver.find_element('xpath', review_num_xpath).text
#                 review_num = review_num.replace(',', '')
#                 review_range = (int(review_num) - 1 ) // 10 + 1
#                     # ex) 41건은 문자열이니까 인트로 바꿔주어야함    # 10개의 리뷰가 2페이지가 되지않게 그냥 1을 더하면 안되고
#                     # 10으로 나눈 몫. 10으로 나누어 떨어졌을 때 1. 근데 그냥 +1하면 => 2가 되어버리니 일단하나빼는 -1
#                 if review_range > 3:        # 3페이지만
#                     review_range = 3
#                 for review_page in range(1, review_range + 1):   # 페이지 수만큼 포문 돌리기
#
#                     review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]/span'.format(review_page)   # 다르네
#                     driver.find_element('xpath', review_page_button_xpath).click()
#                     # 클릭하다 에러날 수 있지만 따로하지않 다른곳에서 하니
#                     time.sleep(0.1)
#
#                     for review_title_num in range(1, 11):   # 리뷰   # 10개씩 있음
#                         review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)   # 리뷰제목 # 뒤에strong 속성은 지움
#                             #리뷰 하나있는 애들은 리스트부분이 없음 (일단은 그대로 진행)
#                         #print('debug02')
#                         driver.find_element('xpath', review_title_xpath).click()  # 클릭
#                         #print('debug01')
#                         time.sleep(0.1)
#
#                         try:
#
#                             review = driver.find_element('xpath', review_xpath).text
#                             titles.append(title)    # 타이틀과 리뷰 같이 저장해줘야 짝이 맞음
#                             reviews.append(review)
#                             # print(review)       # 리뷰를 띄우는
#                             driver.back()         # 뒤로가기(리뷰한번 읽었으면)
#                         except:
#                             print('review', page, title_num, review_title_num)
#                             driver.back()
#             except:
#                 print('review button', page, title_num)    # 케이 없을 수 있으니 빼기
#         df = pd.DataFrame({'titles':titles, 'reviews':reviews})    # 20개 영화 긁어올 때만다 저장하기 # 작업지시서에 있는 것 붙여넣기
#         df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_clip, page), index=False)      #년도, 페이지 # 한 페이지 긁으면 저장
#     except:
#         print('error', page, title_num)             # 케이 없을 수 있으니 빼기




# # 무한스크롤
# while True:  # 무한스크롤 루프
#     driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
#     time.sleep(1)  # 페이지가 완전히 내려갈때까지 대기 -> 페이지 길이가 길면 시간을 증가시킨다
#     curr_height = driver.execute_script("return document.body.scrollHeight")
#     if (curr_height == prev_height):
#         break
#     else:
#         prev_height = driver.execute_script("return document.body.scrollHeight")






