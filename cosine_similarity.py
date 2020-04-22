import pandas as pd
import numpy as np

from pandas.plotting import scatter_matrix

#data frame 제작
df =  pd.read_csv('data.csv')
print(df)

#타이틀 + 인덱스 뽑기
indices = pd.Series(df.index, index=df['name']).drop_duplicates()
print(indices)

from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['name'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#각 인덱스별 유사도 및 1~10순위 출력
sim_scores_table = list()

for idx in range(0, len(df)) :
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores_table.append(sim_scores)

  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  sim_scores = sim_scores[1:11]
  movie_indices = [i[0] for i in sim_scores]
  
print(df['name'].iloc[movie_indices])
