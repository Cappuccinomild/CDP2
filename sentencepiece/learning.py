import pandas as pd
import numpy as np

#회사제공 데이터셋
df =  pd.read_csv('PB.csv')

#dataframe to string
word = []
f = open("./test/test_pb.txt", "w")
for i in range(df.shape[0]):
    f.write(" ".join(list(df.iloc[i])) + "\n")

f.close()

import sentencepiece as spm
spm.SentencePieceTrainer.Train('--input=test/test_pb.txt --model_prefix=m --vocab_size=5000')

'''
#니퍼 데이터셋
df =  pd.read_csv('data_nipper.csv')

#dataframe to string
word = []
f = open("./test/test_nipper.txt", "w")
for name in df['name']:
    f.write(" ".join(list(name)) + "\n")

f.close()

import sentencepiece as spm
spm.SentencePieceTrainer.Train('--input=test/test.txt --model_prefix=m --vocab_size=5000000')
'''
