# TFIDF : 형태소의 출현 빈도 // TF :text 단어 빈도 / I 역순 /  DF: document문서 빈도
# TF-IDF(Term Frequency-Inverse Document Frequency
# = '문장의 유사도' 찾는 것 : '단어의 빈도수'를 볼 것

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer     # 문장에 벡터좌표가 만들어짐.
from scipy.io import mmwrite, mmread                            # 행렬 저장, 행렬 읽기
import pickle


df_reviews = pd.read_csv('./crawling_data/cleaned_informs.csv')
df_reviews.info()

tfidf = TfidfVectorizer()                                       # 좌표
tfidf_matrix = tfidf.fit_transform(df_reviews['clean_informs']) # tfidf_matrix 좌표들의 행렬
print(tfidf_matrix[0].shape)
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(tfidf, f)
mmwrite('./models/tfidf_audio_clip_inform.mtx', tfidf_matrix)   # 좌표값을 만들어 줌