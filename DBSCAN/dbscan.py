from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from pandas.plotting import scatter_matrix

#data frame 제작
df =  pd.read_csv('data.csv')

#타이틀 + 인덱스 뽑기
indices = pd.Series(df.index, index=df['name']).drop_duplicates()

print(indices)

from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['name'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

print(cosine_sim)

clustering = DBSCAN(eps=0.3, min_samples=2).fit(cosine_sim)
label = clustering.labels_

print(clustering.metric)

df['label'] = label
df.to_csv("cluster.csv", index = False, encoding="utf-8-sig")
