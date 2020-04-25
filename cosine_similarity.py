import pandas as pd
import numpy as np

from pandas.plotting import scatter_matrix

#data frame 제작
column_name = ['number', 'title', 'value', 'category', 'link']
df =  pd.read_csv('data.csv', names = column_name)
print(df)

#타이틀 + 인덱스 뽑기
indices = pd.Series(df.index, index=df['title']).drop_duplicates()
print(indices)

from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

#각 인덱스별 유사도 및 상,하위 1~10순위 출력
sim_scores_table = list()

for idx in range(0, len(df)) :
  sim_scores = list(enumerate(cosine_sim[idx]))
  sim_scores_table.append(sim_scores)
  print(df['title'][idx])
  sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
  sim_scores_high = sim_scores[1 : 11]
  sim_scores_low = sim_scores[len(df) - 10 : len(df)]
  product_indices_high = [i[0] for i in sim_scores_high]
  product_indices_low = [i[0] for i in sim_scores_low]
  print('Most Similar Products')
  print(df['title'].iloc[product_indices_high])
  print('\nLeast Similar Products')
  print(df['title'].iloc[product_indices_low])
  print('\n')
