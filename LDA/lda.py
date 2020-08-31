# coding=utf-8
# MF 2020.8.25
import os
import  data_process
import pandas as pd
import  numpy as np
from cntopic import  Topic
import  jieba



def train_lda_and_save(lda_name,documents):
    """
    :param lda_name: 保存lda名字
    :param documents: 训练lda的文档数组
    :return:          lda模型
    """
    # ---------------------------------开始训练LDA模型---------------------------------------
    print("开始训练LDA模型")
    topic = Topic(cwd=os.getcwd())  # 构建词典dictionary
    topic.create_dictionary(documents=documents)  # 根据documents数据，构建词典空间
    topic.create_corpus(documents=documents)  # 构建语料（将文本转为文档-词频矩阵）
    topic.train_lda_model(n_topics=10, epochs=20, fname=lda_name)  # 指定n_topic ，构建LDA话题模型
    print("完成lda模型的训练 并存储")
    #topic.visualize_lda()
    return topic


def load_lda_model(lda_path="output/model/0808_58D7A68C84497105161B73E8FD955D60_lda_model",dict_path="output/dictionary.dict"):
    """
    :param lda_path: lda存储路径
    :return: lda模型
    """
    topic=Topic(cwd=os.getcwd())
    topic.load_dictionary(dictpath=dict_path)
    topic.create_corpus(documents=documents)
    topic.load_lda_model(modelpath=lda_path)
    return topic


def use_lda_generate_data(lda_model_path,dict_path):
    topic=load_lda_model(lda_model_path,dict_path=dict_path)

    # 准备document
    # document=jieba.lcut("体育游戏真有意思")
    # 预测document对应的话题
    # topic.get_document_topics(document)
    # 显示每种话题与对应的特征词之间的关系
    # topic.show_topics()
    # 话题额分布情况
    # topic.topic_distribution()
    # 可视化
    # topic.visualize_lda()

    return








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
