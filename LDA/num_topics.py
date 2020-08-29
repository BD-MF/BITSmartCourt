# coding=utf-8
# MF 2020.8.25

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

#这里需要利用之前的文档分词文件 需要先对中文文档进行分词
fenci_data=pd.read_csv(r"fenci.csv")

#tfidf 矩阵
n_features=1000

#这里是否需要停用词？
stopwordlist=None

tf_vectorizer=CountVectorizer(strip_accents='unicode',
                              max_features=n_features,
                              stop_words=stopwordlist,
                              max_df=0.5,
                              min_df=10)

tf=tf_vectorizer.fit_transform(fenci_data.fenci)  #fenci属性是分词数据的列索引

perplexity=[]
for n_topics in range(60):#一般LDA的topics数在0-60之间
    lda=LatentDirichletAllocation(n_components=n_topics+2,max_iter=100,learning_method='online',
                                  learning_offset=50,random_state=0)
    lda.fit(fenci_data)
    #lda困惑度计算
    perplexity.append(lda.perplexity(fenci_data))
    print(perplexity)
    print("The ",str(n_topics)+"appear")

#困惑度最小的 最适合作为n_topics
Min=1000
n_topics=10#默认为10

for i in range(len(perplexity)):
    if perplexity[i]<=Min:
        Min=perplexity[i]
        n_topics=i+2

print("The best n_topics is ",n_topics)


