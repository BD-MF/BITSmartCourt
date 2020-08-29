# -*- coding:utf-8 -*-
import os
import argparse
import numpy as np
import jieba,re
from gensim import corpora, models, similarities
import json

json_path = "C:\\%shl\\BIT_Affairs\\Lab_Affairs\\Projects\\智慧法院\\算法实现\\five_user_log_sessions.json"
output_path = "C:\\%shl\\BIT_Affairs\\Lab_Affairs\\Projects\\智慧法院\\算法实现\\5_all_contexts.txt"
stop_word_path = "C:\\%shl\\BIT_Affairs\\Lab_Affairs\\Projects\\智慧法院\\算法实现\\stopwords.txt"
jieba_outputs = "C:\\%shl\\BIT_Affairs\\Lab_Affairs\\Projects\\智慧法院\\算法实现\\jieba_contexts.txt"
train = []
"""
将5个session所有案例文本写入一个txt文件中
"""
# with open(json_path,'r',encoding='utf8')as fp:
#     json_data = json.load(fp)
#     for i in json_data:
#         for j in json_data[i]:
#             f = open(output_path,'a',encoding='utf-8')
#             f.write(str(j['contexts']).lstrip('[').rstrip(']'))
#             f.write('\r\n')
#             f.close()

"""
分词
"""
# def load_stopword():
#     f_stop = open(stop_word_path, encoding='utf-8')
#     sw = [line.strip() for line in f_stop]
#     f_stop.close()
#     return sw

# def seg_depart(sentence):
#     sentence_depart = jieba.cut(sentence.strip())
#     stopwords = load_stopword()
#     outstr = ''
#     for word in sentence_depart:
#         if word not in stopwords:
#             outstr += word
#             outstr += " "
#     return outstr

# def segmentation():
#     f = open(output_path, encoding='utf-8')
#     outputs = open(jieba_outputs, 'w', encoding='utf-8')
#     for line in f:
#         line_seg = seg_depart(line.strip())
#         outputs.write(line_seg.strip() + '\n')
#     f.close()
#     outputs.close()

# segmentation()

"""
LDA实现
"""
class LDA:
    def __init__(self, opt):
        self.opt = opt
        self.jieba_path = jieba_outputs
    def train_data(self, path):
        fr = open(path, 'r',encoding='utf-8')
        for line in fr.readlines():
            line = [word.strip() for word in line.split(' ')]
            train.append(line)

    def run(self):
        print('------Reading corpus------ ')
        self.train_data(self.jieba_path)
        print('Number of documents is: %d' % len(train))
        print('------Building Dictionary------ ')
        dictionary = corpora.Dictionary(train)
        print('Length of dictionary is: %d' % len(dictionary))
        corpus = [dictionary.doc2bow(text) for text in train]
        print('------Calculating TF-IDF------')
        corpus_tfidf = models.TfidfModel(corpus)[corpus]
        print('------Training Model------')
        lda = models.LdaModel(corpus_tfidf, num_topics=self.opt.num_topics, id2word=dictionary,
                        alpha=0.01, eta=0.01, minimum_probability=0.001,
                        update_every=1, chunksize=100, passes=1)
        if self.opt.save:
            lda.save("LDA.model")
            print('------Model Saved------')
        topic_list = lda.print_topics(self.opt.num_topics)
        print("主题的单词分布为：\n")
        for topic in topic_list:
            print(topic)

if __name__ == '__main__':
    # Hyper Parameters
    parser = argparse.ArgumentParser()
    parser.add_argument('--num_topics', default=10, type=int)
    parser.add_argument('--save', default=False, type=bool)
    opt = parser.parse_args()
    # train model
    lda = LDA(opt)
    lda.run()