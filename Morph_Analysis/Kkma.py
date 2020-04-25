from numpy import dot
from numpy.linalg import norm
import numpy as np
import pandas as pd
data = pd.read_csv('data.csv', low_memory = False)

def kkmtest(string):
    from konlpy.tag import Kkma
    kkma = Kkma()

    term_list = kkma.morphs(string)


    for term in string:
        if term in ['(', ')', '[', ']', '/', '_', ')/', '/(', '-', ')-']:
            if term in term_list:
                term_list.remove(term)
    term_list.sort()
    return " ".join(term_list)

for pname in data['test']:
    t = pname
    kom = kkmtest(pname)
    data.loc[data['test'] == t, 'test'] = kom

data['test'].isnull().sum()
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(data['test'])
print(tfidf_matrix.shape)

from sklearn.metrics.pairwise import linear_kernel
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
indices = pd.Series(data.index, index=data['test']).drop_duplicates()

def get_recommendations(test, cosine_sim = cosine_sim):
    idx = 1000
    print(idx)
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:1501]
    movie_indices = [i[0] for i in sim_scores]

    print(cosine_sim)

    return data['test'].iloc[movie_indices]

kkma_test = get_recommendations('니퍼 전자용미니 KM-037 5인치 게이바')

f = open('kkma.csv', 'w', encoding = 'utf-8-sig')

f.write('상품코드, 가격, test, 카테고리, 링크\n')

for i in kkma_test.index:
    code = data.loc[i, '상품코드'].astype(str)
    price = data.loc[i, '가격'].astype(str)
    test = data.loc[i, 'test']
    cate = data.loc[i, '카테고리']
    link = data.loc[i, '링크']
    f.write(code + ", " + price + ", "+ test + ", " + cate + ", " + link + "\n")

f.close()
