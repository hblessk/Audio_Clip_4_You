import pandas as pd
from konlpy.tag import Okt
import re

df = pd.read_csv('./crawling_data/audio_clip_1_2470.csv')   # 컨캣한 파일 불러오기
df.info()
print(df.head())

df_stopwords = pd.read_csv('./stopwords.csv', index_col=0)  # 불용어


okt = Okt()
df['clean_informs'] = None
count = 0
for idx, inform in enumerate(df.informs):
    count += 1
    if count % 10 == 0:     # 10개마다 점찍고
        print('.', end='')
    if count % 1000 == 0:   # 10줄마다 줄바꿈 (10*100=1000)
        print()
    inform = re.sub('[^가-힣 ]', ' ', inform)     # 한글만 남긴
    df.loc[idx, 'clean_informs'] = inform
    token = okt.pos(inform, stem=True)      # 형태소 단위로 쪼갠    # 명사, 동사, 형용사 빼고 없애기
    df_token = pd.DataFrame(token, columns=['word', 'class'])    # 토큰을 데이터 프레임으로 만들 것
    df_token = df_token[(df_token['class'] == 'Noun') |          # 조건인덱싱 #클래스 컬럼의 값이 명사인 것
                        (df_token['class'] == 'Verb') |
                        (df_token['class'] == 'Adjective')]      # 아름다운 => 아름답다와 같은 형용사는 의미 있.

 # 불용어 제거
    words = []
    for word in df_token.word:                                  # 컬럼 인덱싱! 함수호출과 다른거는 괄호, 클래스 변수도 .으로 접근할 수 있
        if len(word) > 1:
            if word not in list(df_stopwords.stopword):
                words.append(word)
    cleaned_sentence = ' '.join(words)
    df.loc[idx, 'clean_informs'] = cleaned_sentence             # clean_informs 컬럼에 넣기
print(df.head(10))
df.dropna(inplace=True)
df.to_csv('./crawling_data/cleaned_informs.csv', index=False)   # cleaned_informs 파일명으로 저장