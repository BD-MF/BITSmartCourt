import numpy as np
import pandas as pd
from LDA.data_process import read_json_data
json_file_path="five_user_log_sessions.json"
'''
    从点击的文档抽取主题：
    我们使用文档中讨论的主题构建用户画像：
        首先，从内部网搜索的查询日志中提取用户点击的文档。
        之后，我们使用LDA从用户点击的文档（标记为D）中自动提取潜在主题（标记为Z）。在使用用户点击的文档训练了LDA模型之后，使用该模型为集合中其余文档提取主题。
        最后，每个文档都被描述为主题的多项分布（表示为P(Z|D)），其中每个主题被表示为整个词汇表上的多项分布。
'''



def extract_theme_from_click_file():
    users_click_files=generate_click_data_from_json("click")
    users_other_files=generate_click_data_from_json("noclick")

    return

'''
    构建点击用户画像函数 
    将时间点击用户画像表示为主题上的多项分布。
    具体来说，用户集合表示为U。令u为U的实例。
    我们将用户u的点击用户画像定义为主题Z上的分布。
'''
def click_user_portrait(user_id,Z,N,alph,tDci,Pzd,Dc=[]):
    """
    :param user_id: 用户id
    :param Dc:      为用户u在当前搜索会话中点击的文档的集合
    :param Z:       全部主题
    :param N:       归一化因子
    :param alph:    衰减参数 >=0  and <=1
    :param tDci:    是用户u在搜索会话中点击文档dci的顺序
    :param Pdciz:   文档i属于主题z的概率[文档数][主题数]
    :return:        点击用户画像dict
    """
    result={}
    for i,z in enumerate(Z): #遍历每个主题z 去计算p(z|qi)
        pc_z_qi=0
        lamdai=alph**(tDci**-1)
        for j,dci in enumerate(Dc):#遍历点击文档集合
            pc_z_qi+=lamdai*Pzd[i][j]
        pc_z_qi/=N
        result[z]=pc_z_qi
    return result

'''
    从json中获取相应的数据
'''
def generate_click_data_from_json(type="click"):
    users_sessions_data=read_json_data(json_file_path)
    user_click_contexts={}
    for user_id in users_sessions_data.keys():
        user_sessions=users_sessions_data[user_id]
        user_click_context=[]
        if type=="click":
            for user_session in user_sessions:
                if user_session.case_type=="查看案件详情":
                    user_click_context.append(user_session.contexts)
            user_click_contexts[user_id]=user_click_context
        else:
            for user_session in user_sessions:
                if user_session.case_type!="查看案件详情":
                    user_click_context.append(user_session.contexts)
            user_click_contexts[user_id]=user_click_context
    return user_click_contexts





