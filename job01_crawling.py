#자연어기반 오디오 소설 추천시스템
from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time

#크롤링코드 만든다음에 크롤링 분담하여
options = webdriver.ChromeOptions()

options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)    # 드라이버 만들어놓

# 어디를 긁을 거냐면 : 네이버 영화 리뷰 -> 비슷한 리뷰를 가지고 있는 영화를 추천해줄 것 (ex)겨울왕국)
# 추천시스템 그전 알고리즘 방식 - 분유를 샀다면 기저귀를 살 가능성이 높. 포인트카드만들며 구매정보 활용할 수 있도록 사인하게됨 # 그 장바구니 정보로 : 통계적인 방법
# 인공지능. 자연어처리가 된다는 것. 말은 통계로 안됨(수식) 넷플릭스 추천컨텐츠 목록에 올라오는 것들
# 추천이라는 건 노출 많이 시켜주는 것. 원래 아마존에서 안사던 사람인데 띄워줘서 사는 30프로

url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open=2022&page=1'     # 페이지

# 깃만들기 VCS > share project on github
# 팀장 : 위에 없이 크롤링 코드 만들기만 하고 안내만 - 컬럼명, 파일명 통일되도록
# 천천히 해도 이번 주 안으로 끝날 듯? 목표는 금요일
# 멈추지말고 계속갑시다 지치면 안돼!!

# x_path 원본 모음
#       '//*[@id="old_content"]/ul/li[13]/a'    # 제목
#       '//*[@id="movieEndTabMenu"]/li[5]/a'    # 리뷰 버튼
#       '//*[@id="movieEndTabMenu"]/li[6]/a'    # 리뷰 버튼 (동영상 탭 있는 버전)
#       '//*[@id="reviewTab"]/div/div/ul/li[2]/a/strong'# 리뷰타이틀    # 리뷰 10개씩 있음. 페이지 수 늘어나고
#       //*[@id="content"]/div[1]/div[4]/div[1]/div[4]  # 리뷰 텍스트전체 포함된 부분
# //*[@id="pagerTagAnchor1"]/span # 리뷰 페이지 버튼


review_button_xpath = '//*[@id="movieEndTabMenu"]/li[6]/a'  # 리뷰 버튼 누르기 # 6번이 더 많으니 일단 6번으로 #어차피 바뀌지않음 포문 밖으로 빼겠음
review_num_xpath = '//*[@id="reviewTab"]/div/div/div[2]/span/em'  # 리뷰 건수 # 얘도 포문에서 빼고
review_xpath = '//*[@id="content"]/div[1]/div[4]/div[1]/div[4]'   # 리뷰 텍스트전체 포함된 부분 # 이건 중괄호 안해도 되나?


your_year = 2018
for page in range(33, 51):    # (1~31) 페이지 = i  # i 값으로 페이지 접근할 것이니 몇 까지 있는지 확인
    url = 'https://movie.naver.com/movie/sdb/browsing/bmovie.naver?open={}&page={}'.format(your_year, page) # 페이지
    titles = []           # 받아올 것 1 = 영화 20개 긁어을 때마다 저장합시다, 여기다 어펜드 시켜야하는
    reviews = []          # 받아올 것 2 = 영화 20개 긁어을 때마다 저장합시다, 여기다 어펜드 시켜야하는
    try:

        for title_num in range(1, 21):                  # 제목 j   # X_path 따기 20개씩 있으니 for문 20개씩 돌아야.
            driver.get(url)                     # 드라이버 겟 여기서 하니까 계속 다시함 (새로고침)
            time.sleep(0.1)                     # 열고 잠시 기다려주고

            movie_title_xpath = '//*[@id="old_content"]/ul/li[{}]/a'.format(title_num)    # 제목

            title = driver.find_element('xpath', movie_title_xpath).text    # 텍스트만 가져오면 됨

            print('title', title)
            driver.find_element('xpath', movie_title_xpath).click()  # 클릭
            time.sleep(0.1)
            # print(title)
            # print('debug01')

            try:    # 리뷰 누르다가 에러나는 것이니
                driver.find_element('xpath', review_button_xpath).click()      # 클릭
                time.sleep(0.1)

                review_num = driver.find_element('xpath', review_num_xpath).text
                review_num = review_num.replace(',', '')
                review_range = (int(review_num) - 1 ) // 10 + 1
                    # ex) 41건은 문자열이니까 인트로 바꿔주어야함    # 10개의 리뷰가 2페이지가 되지않게 그냥 1을 더하면 안되고
                    # 10으로 나눈 몫. 10으로 나누어 떨어졌을 때 1. 근데 그냥 +1하면 => 2가 되어버리니 일단하나빼는 -1
                if review_range > 3:        # 3페이지만
                    review_range = 3
                for review_page in range(1, review_range + 1):   # 페이지 수만큼 포문 돌리기

                    review_page_button_xpath = '//*[@id="pagerTagAnchor{}"]/span'.format(review_page)   # 다르네
                    driver.find_element('xpath', review_page_button_xpath).click()
                    # 클릭하다 에러날 수 있지만 따로하지않 다른곳에서 하니
                    time.sleep(0.1)

                    for review_title_num in range(1, 11):   # 리뷰   # 10개씩 있음
                        review_title_xpath = '//*[@id="reviewTab"]/div/div/ul/li[{}]/a'.format(review_title_num)   # 리뷰제목 # 뒤에strong 속성은 지움
                            #리뷰 하나있는 애들은 리스트부분이 없음 (일단은 그대로 진행)
                        #print('debug02')
                        driver.find_element('xpath', review_title_xpath).click()  # 클릭
                        #print('debug01')
                        time.sleep(0.1)

                        try:

                            review = driver.find_element('xpath', review_xpath).text
                            titles.append(title)    # 타이틀과 리뷰 같이 저장해줘야 짝이 맞음
                            reviews.append(review)
                            # print(review)       # 리뷰를 띄우는
                            driver.back()         # 뒤로가기(리뷰한번 읽었으면)
                        except:
                            print('review', page, title_num, review_title_num)
                            driver.back()
            except:
                print('review button', page, title_num)    # 케이 없을 수 있으니 빼기
        df = pd.DataFrame({'titles':titles, 'reviews':reviews})    # 20개 영화 긁어올 때만다 저장하기 # 작업지시서에 있는 것 붙여넣기
        df.to_csv('./crawling_data/reviews_{}_{}page.csv'.format(your_year, page), index=False)      #년도, 페이지 # 한 페이지 긁으면 저장
    except:
        print('error', page, title_num)             # 케이 없을 수 있으니 빼기









