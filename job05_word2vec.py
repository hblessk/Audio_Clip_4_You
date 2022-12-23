import pandas as pd
from gensim.models import Word2Vec

inform_word = pd.read_csv('./crawling_data/cleaned_informs.csv')
inform_word.info()

# 타이틀 말고 정보 뽑기
one_sentence_informs = list(inform_word['clean_informs']) # 리스트로
cleaned_tokens = []
for sentence in one_sentence_informs:     # 문자열이 들어가 있는 걸 형태소 단위로 자름
    token = sentence.split()              # 띄어쓰기 기준으로 다 자르기
    cleaned_tokens.append(token)


# 임베딩 모델 만들 것. 유사한 단어들을 근처에 배치하는 워드투벡
# 단어를 벡터화 해주는 임베딩모델 Word2vec # 각 소설의 정보를 한 문장씩 = 형태소들의 리스트로 만들어서 줄 것
embedding_model = Word2Vec(cleaned_tokens, vector_size=100,    # 형태소 개수만큼 차원이 만들어짐. # 벡터 사이즈 100으로 차원축소
                            window=4, min_count=7,             # => min 20 =>10 => 7
                            workers=4, epochs=100, sg=1)


# 유사한 단어 많이 있는 리뷰 추천
embedding_model.save('./models/word2vec_audio_clip_inform.model')
print(list(embedding_model.wv.index_to_key))
print(len(embedding_model.wv.index_to_key))     # 몇개 있는 지 보려면
