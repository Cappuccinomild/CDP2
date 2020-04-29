import pandas as pd
import numpy as np
import sentencepiece as spm
import re

def clenText(readData):
    #텍스트에 포함되어 있는 특수 문자 제거
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)

    return text

def recover(tokens):
    sent = ''.join(tokens)
    sent = sent.replace('_', ' ')
    sent = sent.replace("▁", " ")
    return sent

sp = spm.SentencePieceProcessor()
sp.Load("m.model")

df =  pd.read_csv('data_km.csv')

sentences = []
for text in df['name']:
    
    sentences.append(clenText(recover(sp.EncodeAsPieces(text))))

df['name'] = sentences

df.to_csv("tokenized.csv", index = False, encoding="utf-8-sig")
