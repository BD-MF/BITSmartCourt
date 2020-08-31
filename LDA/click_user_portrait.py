import numpy as np
import pandas as pd
from LDA.data_process import read_json_data
json_file_path="five_user_log_sessions.json"
from LDA.data_process import chineseSentenceSplit
from LDA.lda import train_lda_and_save,load_lda_model,use_lda_generate_data
import json
import re
'''
    从点击的文档抽取主题：
    我们使用文档中讨论的主题构建用户画像：
        首先，从内部网搜索的查询日志中提取用户点击的文档。
        之后，我们使用LDA从用户点击的文档（标记为D）中自动提取潜在主题（标记为Z）。在使用用户点击的文档训练了LDA模型之后，使用该模型为集合中其余文档提取主题。
        最后，每个文档都被描述为主题的多项分布（表示为P(Z|D)），其中每个主题被表示为整个词汇表上的多项分布。
'''



def extract_theme_from_click_file():
    users_click_files=read_click_contexts_from_json("users_click_contexts_alldata.json")
    users_other_files=read_click_contexts_from_json("users_noclick_contexts_alldata.json")
    users_click_portrait_result={}
    for user in users_click_files.keys():
        Z = []
        lda_model=train_lda_and_save(user+"_lda_model",users_click_files[user])
        topics=lda_model.show_topics()
        key_words_percent={}
        for topic in topics:
            loc=topic[0]
            percent_words_dict={}
            print("topic[1]: ",topic[1])
            percent_words=str(topic[1]).split("\" + ")
            print("percent_words: ",percent_words)
            for perc_word in percent_words:
                print("perc_word: ",perc_word)
                percent=perc_word.split("*\"")[0]
                print("percent: ",percent)
                word = perc_word.split("*\"")[1]
                print("word: ",word)
                percent_words_dict[word]=percent
            key_words_percent[loc]=percent_words_dict
        users_click_portrait_result[user]=key_words_percent
            #Z.append(loc)

        # click_user_portrait_result=click_user_portrait()
        # users_click_portrait_result[user]=click_user_portrait_result

    jss = json.dumps(users_click_portrait_result, ensure_ascii=False)
    json_sessions = open("click_user_portrait.json", 'w')
    json_sessions.write(jss)
    json_sessions.close()
    print("OK")
    return users_click_portrait_result


        # print(topics)
        # for texts in users_other_files[user]:
        #     print(lda_model.get_document_topics(texts))
            # for text in texts:
            #     print(lda_model.topic_distribution(text))
            #     print(text)
            #     print(lda_model.get_document_topics(text))

'''
    构建点击用户画像函数 
    将时间点击用户画像表示为主题上的多项分布。
    具体来说，用户集合表示为U。令u为U的实例。
    我们将用户u的点击用户画像定义为主题Z上的分布。
'''
def click_user_portrait(user_id,Z=[],N=1000,alph=0.5,tDci=[],Pzd=[],Dc=[]):
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
def read_click_contexts_from_json(json_path="users_click_contexts_data.json"):
    with open(json_path, 'r', encoding="utf-8") as f:
        users_click_contexts_data =json.load(f)
    f.close()
    return users_click_contexts_data

def generate_click_contexts_from_json(name,type="click"):
    print("生成"+type+"文档数据")
    users_sessions_data=read_json_data(json_file_path)
    #num=0
    user_click_contexts={}
    for user_id in users_sessions_data.keys():
        #num=0
        user_sessions=users_sessions_data[user_id]
        user_click_context=[]
        if type=="click":

            for user_session in user_sessions:
                if user_session.kind=="查看案件详情" and len(user_session.contexts)>0:
                    for t in user_session.contexts:
                        user_click_context.append(chineseSentenceSplit(t))
                        # num+=1
                        # if num>5:
                        #     break
                    #user_click_context.append(chineseSentenceSplit(t) for t in user_session.contexts)
            user_click_contexts[user_id]=user_click_context
        else:

            for user_session in user_sessions:
                if user_session.kind!="查看案件详情" and len(user_session.contexts)>0:
                    for t in user_session.contexts:
                        user_click_context.append(chineseSentenceSplit(t))
                        # num += 1
                        # if num > 5:
                        #     break
                    #user_click_context.append(chineseSentenceSplit(t) for t in user_session.contexts)
            user_click_contexts[user_id] = user_click_context

    jss = json.dumps(user_click_contexts, ensure_ascii=False)
    json_sessions = open(name, 'w')
    json_sessions.write(jss)
    json_sessions.close()
    print("OK")
    return user_click_contexts




if __name__=="__main__":
    #
    users_click_files = generate_click_contexts_from_json( "users_click_contexts_alldata.json","click")
    print("用户点击文档数据生成OK！")
    users_other_files = generate_click_contexts_from_json(  "users_noclick_contexts_alldata.json","noclick")
    print("用户非点击文档数据生成OK！")
    extract_theme_from_click_file()
    print("main 运行结束")
