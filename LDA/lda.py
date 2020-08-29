# coding=utf-8
# MF 2020.8.25
import os
import  data_process
import num_topics
import pandas as pd
import  numpy as np
from cntopic import  Topic
import  jieba
documents=pd.read_csv("文档位置")



documents=[data_process.chineseSentenceSplit(txt) for txt in documents['context']]

#---------------------------------开始训练LDA模型---------------------------------------
topic=Topic(cwd=os.getcwd())#构建词典dictionary
topic.create_dictionary(documents=documents)#根据documents数据，构建词典空间
topic.create_corpus()#构建语料（将文本转为文档-词频矩阵）
topic.train_lda_model(n_topics=10,epochs=20,fname="lda_model")#指定n_topic ，构建LDA话题模型

topic.visualize_lda()



#--------------------------------使用LDA模型------------------------------------------
#准备document
#document=jieba.lcut("体育游戏真有意思")
#预测document对应的话题
#topic.get_document_topics(document)
#显示每种话题与对应的特征词之间的关系
#topic.show_topics()
#话题额分布情况
#topic.topic_distribution()
#可视化
#topic.visualize_lda()

#存储与导入lda模型   默认是存储的
#topic2=Topic(cwd=os.getcwd())
#topic2.load_dictionary(dictpath="path")
#topic2.create_corpus(documents=documents)
#topic2.load_lda_model(modelpath="path")
