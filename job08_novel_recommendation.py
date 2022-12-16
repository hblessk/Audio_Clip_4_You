# 모델 저장 완료, 유사한 문장을 가진 소설 추천
# 10개 찾아서 영화추천 해보겠음
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

# 함수 만들기
def getRecommendation(cosin_sim):                   # 코사인 유사도 값이 다 들어있음
    simScore = list(enumerate(cosin_sim[-1]))       # 인덱스 붙이고      # enumerate : 소팅하면서 인덱스  # [-1] : 어차피 하나만 들어있어서 0이어도 됨.. 인덱싱을 한번 해줘야해서 한번 해준 것
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)       # 정렬(sort), 내림차순 되도록 = 큰값 먼저나오게 (reverse)
    simScore = simScore[:11]                        # 0번~10번까지 => 가장 유사한 11개. => 왜 11개일까?
                                                    # 이유 : tfidx에 겨울왕국(자신) 있을거고, 둘다 코사인심하면 1번(?)이 자기자신이 됨. 11개뽑고 같은 겨울왕국(자신) 빼고 다른 10개를 추천
    audiobook_idx = [i[0] for i in simScore]                # 10개 남기고 i로 받아서 영화의 인덱스 뽑아낸 것 # 무비idx에
    recAudioClipList = df_informs.iloc[audiobook_idx, 0]    # 0 = 영화 타이틀.
    return recAudioClipList                                 # 타이틀 11개 리턴

df_informs = pd.read_csv('./crawling_data/cleaned_informs.csv')
tfidf_matrix = mmread('./models/tfidf_audio_clip_inform.mtx').tocsr()        # models/tfidf_movie_review.mtx
with open('./models/tfidf.pickle', 'rb') as f:
    tfidf = pickle.load(f)       #f


# ## 1. 오디오클립 제목 이용
# audiobook_idx = df_informs[df_informs['titles']=='오리엔트 특급 살인'].index[0]      # d..f에서 겨울왕국  # ['titles'] #인덱스 0번째?
# cosin_sim = linear_kernel(tfidf_matrix[audiobook_idx], tfidf_matrix)               # 겨울왕국과 리스트에 있는 모든 영화의 유사도 값.   # 리뷰 4천여개 9만9천여개 tfidf값을 쫙만들었고 문장의 개수만큼 생겼을 것
# print(cosin_sim)
# recommendation = getRecommendation(cosin_sim)
# print(recommendation[1:11])


# ## 2. 오디오클립 key word 이용
# # 키워드 이용하여
# embedding_model = Word2Vec.load('./models/word2vec_audio_clip_inform.model')
# key_word = '로맨스'           # 여기서 단어 바꾸면서  # ex)어벤져스     # tf에 가중치 준 것
# sim_word = embedding_model.wv.most_similar(key_word, topn=10)            # 유사단어 임베딩 모델에게
# words = [key_word] #* 10        # 문장이 아닌 키워드. 반복 인위적으로 늘릴 것    # 나중에 *10빼신듯?
# for word, _ in sim_word:        # 유사단어 10개 뽑았었고 여깄는 단어들도 word에 추가
#     words.append(word)
# print(words)
#
# # 위까진 '유사 단어'를 찾은거고 이걸 문장으로 만들 것. 이유 : tfidf에선 반복 횟수가 중요하기에
# sentence = []
# count = 11
# for word in words:               # 단어를 하나씩 꺼내고 카운트를 곱해서 더해줌  # 빈 리스트에 저장(=sentence)
#     sentence = sentence + [word] * count
#     count -= 1                   # count 에서 1을 뺀 값 /
# sentence = ' '.join(sentence)
# print(sentence)
# sentence_vec = tfidf.transform([sentence])               # sentence에 넣기 위해 tfidf값을 찾아야함 # 핏이 한번 되어서 fit은 하지않음
# cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
# recommendation = getRecommendation(cosin_sim)
#
# # 제일 유사한 게 자기자신 아님. 슬라이싱 안하고 처음부터 봄
# print(recommendation)                                   # 가장 유사한게 자기 자신이 아님
# #형태소 시각화 해봐야 => job09



##3. 오디오클립 문장으로 추천
sentence = '소름 돋는 반전'          # 얘도 벡터화하고 전처리해야. => 매트릭스 구하고, 코사인 매트릭스
review = re.sub('[^가-힣 ]', ' ', sentence)
okt = Okt()
token = okt.pos(review, stem=True)
df_token = pd.DataFrame(token, columns=['word', 'class'])
df_token = df_token[(df_token['class']=='Noun') |
                    (df_token['class']=='Verb') |         #Verc라고 썼던
                    (df_token['class']=='Adjective')]
words = []
for word in df_token.word:                               # 불용어 처리는 생략
    if 1 < len(word):
        words.append(word)
cleaned_sentence = ' '.join(words)
print(cleaned_sentence)

sentence_vec = tfidf.transform([cleaned_sentence])       # 센텐스 벡터 만들기 # 핏트랜스폼 다시하면 안되고 tfidf에 썼던 그 모델(?) 다시써야
cosin_sim = linear_kernel(sentence_vec, tfidf_matrix)
recommendation = getRecommendation(cosin_sim)
print(recommendation)






# 추천이 잘 되는 건지 안된 건지 그건 확인해보는 수 밖에
# 내용을 봐도 왜 추천됐는지 모르겠다면 한문장안에서 출현빈도가 많은 아이일 수록 크고 나타내주는 워드틀라우드
# 계산하는 데 방해가 되는건 스탑워즈 추가하여 다시돌려볼 수도 있고











