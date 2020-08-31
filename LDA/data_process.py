# coding=utf-8
# MF 2020.8.25
import numpy as np
import pandas as pd
import jieba
import re
import os
from session import  session
import  xml.parsers
import json
import  xml.etree.ElementTree as ET



logsfilepath="/Users/mafang/Desktop/SmartCourt/Searchlog"
click_log_file_path_SAT_Click="/Users/mafang/Desktop/SmartCourt/Click/SAT-Click"
click_log_file_path_Click_Search="/Users/mafang/Desktop/SmartCourt/Click/Click_Search"


def parse_sessions_from_click_log(click_log_file_path):
            users_search_logs = {}
            user_files = os.listdir(click_log_file_path)
            user_id = ""
            sessions = []  # a user's all log session
            for file in user_files:  # 遍历每个用户的日志文件
                if not os.path.isdir(file):  # 此时不是文件夹才打开
                    userid = file[0:37]
                    user_id = userid
                    f = open(click_log_file_path + "/" + file, 'rb')  # ,encoding='utf-8'
                    lines = f.readlines()
                    str = ""
                    for line in lines:
                        line = line.decode("utf8", "ignore")
                        str = str + line
                    f.close()
                    matchstr = r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)  --  (案例研判检索分析|案例研判组合检索|查看案件详情)  --(.*)"
                    matcheds = re.findall(matchstr, str)

                    for per in matcheds:
                        # print(per)
                        date_time = per[0] + "-" + per[1] + "-" + per[2] + " " + per[3] + ":" + per[4] + ":" + per[5]
                        kind = per[6]
                        key_str = ""
                        case_type = ""
                        view_id = ""
                        view_folder = ""
                        location_list = ""
                        ids = []
                        if kind == "查看案件详情":
                            view_id = None
                            splits = per[7]
                            splits = re.split("  --   所在列表位置 : ", splits)
                            url = splits[0].strip()
                            urls = re.split("/", url)
                            case_type = urls[1]
                            if case_type == "case" or case_type == "alcase":
                                view_id = urls[2]
                            else:  # casews
                                view_folder = urls[2]
                                view_id = urls[3]
                            location_list = re.split("\\r", splits[1])[0]

                        elif kind == "案例研判检索分析":
                            keystr = "" + per[7]
                            result_nul = keystr.find("结果  : []")
                            if result_nul == -1:
                                keystr = re.split("结果  : \[{\"resultIds\":\[\"", keystr)[1]
                                ids = re.split("\"\],\"searchType\":", keystr)[0]
                                ids = re.split("\",\"", ids)
                                key_str = re.split(",\"cfield\":\"", per[7])[1]
                                key_str = re.split("\",\"value\":\"", key_str)[0]
                            else:
                                ids = []
                        else:  # 案例研判组合检索
                            morekeystr = "" + per[7]
                            result_nul = morekeystr.find("结果  : \[\]")
                            if result_nul != -1:
                                keystrs = re.split("结果  : \[{\"resultIds\":\[\"", morekeystr)[1]
                                ids = re.split("\],\"searchType\":\"QWAL\"\},\{\"resultIds\":\[", keystrs)
                                ids1 = ids[0]
                                ids2 = ids[1]
                                ids2 = re.split("\"\],\"searchType\":", ids2)[0]
                                ids1 = re.split("\",\"", ids1)
                                ids2 = re.split("\",\"", ids2)
                                ids = ids1 + ids2
                                key_str = re.split(",\"cfield\":\"", morekeystr)[1]
                                key_str = re.split("\",\"value\":\"", morekeystr)
                        se = session(user_id=userid, date=date_time, kind=kind, keystr=key_str, case_type=case_type,
                                     view_id=view_id, view_folder=view_folder, location_list=location_list,
                                     result_ids=ids,
                                     contexts=None)
                        sessions.append(se)
                    users_search_logs[user_id]=sessions
            return users_search_logs



#从内部网搜索的查询日志中提取用户点击的文档session信息
def parse_sessions_from_log(logfilepath):
    all_users_files = os.listdir(logfilepath)
    users_search_logs = {}  # a dict with  userid: sessions

    for all_file in all_users_files:  # 遍历所有用户的searchlog 文件夹 这里是五个用户
        if os.path.isdir(logfilepath + "/" + all_file):  # 判断是否是文件夹，是文件夹才打开
            user_files = os.listdir(logfilepath + "/" + all_file)
            user_id = ""
            sessions = []  # a user's all log session
            for file in user_files:  # 遍历每个用户的日志文件
                if not os.path.isdir(file):  # 此时不是文件夹才打开
                    userid = file[0:37]
                    user_id = userid
                    f = open(logfilepath + "/" + all_file + "/" + file, 'rb')  # ,encoding='utf-8'
                    lines = f.readlines()
                    str = ""
                    for line in lines:
                        line = line.decode("utf8", "ignore")
                        str = str + line
                    f.close()
                    matchstr = r"(\d\d\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)  --  (案例研判检索分析|案例研判组合检索|查看案件详情)  --(.*)"
                    matcheds = re.findall(matchstr, str)

                    for per in matcheds:
                        #print(per)
                        date_time = per[0] + "-" + per[1] + "-" + per[2] + " " + per[3] + ":" + per[4] + ":" + per[5]
                        kind = per[6]
                        key_str=""
                        case_type=""
                        view_id=""
                        view_folder=""
                        location_list=""
                        ids=[]
                        if kind == "查看案件详情":
                            view_id = None
                            splits = per[7]
                            splits = re.split("  --   所在列表位置 : ", splits)
                            url = splits[0].strip()
                            urls = re.split("/", url)
                            case_type = urls[1]
                            if case_type == "case" or case_type == "alcase":
                                view_id = urls[2]
                            else:  # casews
                                view_folder = urls[2]
                                view_id = urls[3]
                            location_list = re.split("\\r", splits[1])[0]

                        elif kind == "案例研判检索分析":
                            keystr = "" + per[7]
                            result_nul = keystr.find("结果  : []")
                            if result_nul == -1:
                                keystr = re.split("结果  : \[{\"resultIds\":\[\"", keystr)[1]
                                ids = re.split("\"\],\"searchType\":", keystr)[0]
                                ids = re.split("\",\"", ids)
                                key_str=re.split(",\"cfield\":\"",per[7])[1]
                                key_str=re.split("\",\"value\":\"",key_str)[0]
                            else:
                                ids = []
                        else:  # 案例研判组合检索
                            morekeystr = "" + per[7]
                            result_nul = morekeystr.find("结果  : \[\]")
                            if result_nul != -1:
                                keystrs = re.split("结果  : \[{\"resultIds\":\[\"", morekeystr)[1]
                                ids = re.split("\],\"searchType\":\"QWAL\"\},\{\"resultIds\":\[", keystrs)
                                ids1 = ids[0]
                                ids2 = ids[1]
                                ids2 = re.split("\"\],\"searchType\":", ids2)[0]
                                ids1 = re.split("\",\"", ids1)
                                ids2 = re.split("\",\"", ids2)
                                ids = ids1 + ids2
                                key_str = re.split(",\"cfield\":\"", morekeystr)[1]
                                key_str = re.split("\",\"value\":\"", morekeystr)
                        se = session(user_id=userid, date=date_time, kind=kind, keystr=key_str, case_type=case_type,
                                     view_id=view_id,view_folder=view_folder, location_list=location_list, result_ids=ids,
                                     contexts=None)
                        sessions.append(se)
            users_search_logs[user_id] = sessions
    return users_search_logs



#进行中文分词 输入一篇文章
def chineseSentenceSplit(string): #return [n]  n 为一句评论中分词个数
    #print(string)
    data = clean_str(string)
    seg_list = jieba.cut(data)  # 默认是精确模式
    tokens = [t for t in seg_list if len(t) > 1]  # 剔除单字
    segList = []
    for s in tokens:
        s = clean_str(s)
        segList.append(s)
    return segList


# 句子清洗
def clean_str(string):
    string = re.sub(r"\\", "", string)
    string = re.sub(r"\'", "", string)
    string = re.sub(r"\"", "", string)
    string = re.sub(r"\r\n", "", string)
    string = re.sub(r"\r", "", string)
    string = re.sub(r"\,", "", string)
    string = re.sub(r"\.", "", string)
    string = re.sub(r"\，", "", string)
    string = re.sub(r"\。", "", string)
    string = re.sub(r"\（", "", string)
    string = re.sub(r"\）", "", string)
    string = re.sub(r"\(", "", string)
    string = re.sub(r"\)", "", string)
    string = re.sub(r"\“", "", string)
    string = re.sub(r"\”", "", string)
    return string.strip()


def get_documents_from_sessions(save_name,logsfilepath):
    users_sessions = parse_sessions_from_click_log(logsfilepath)
    dict_sessions={}
    for key in users_sessions.keys():
        click_documents_ids = []
        search_documents_ids = []
        user_sessions = users_sessions[key]
        for one_session in user_sessions:
            if one_session.kind == "查看案件详情":  # 查看案件详情 属于用户点击事件 用于构建点击用户画像
                if one_session.case_type == "casews":
                    text_folder = one_session.view_folder
                    text_id = one_session.view_id
                    texts = get_documents_from_folder_id(folder_id=text_folder, search=2, text_id=text_id, ids=[])
                else:  # case_type=alcase or case
                    text_id = one_session.view_id
                    texts = get_documents_from_folder_id(folder_id=text_id, search=1, text_id=None, ids=[])
            else:  # 案例研判检索分析 or 案例研判组合检索  属于用户查询事件 用于构建查询用户画像
                ids = one_session.result_ids
                texts = get_documents_from_folder_id(folder_id=None, search=3, text_id=None, ids=ids)

            one_session.contexts = texts


    for key in users_sessions.keys():
        user_sessions = users_sessions[key]
        new_user_sessions=[]
        for se in user_sessions:
            new_user_sessions.append(se.__dict__)
        dict_sessions[key]=new_user_sessions
    jss=json.dumps(dict_sessions,ensure_ascii=False)
    json_sessions=open(save_name,'w')
    json_sessions.write(jss)
    json_sessions.close()
    print("OK")


    return

documents_path="/Users/mafang/Desktop/SmartCourt/original_text/original text"

def get_documents_from_folder_id(folder_id=None,search=1,text_id=None,ids=[]):
    """
    :param folder_id:  案例文件夹id
    :param search:     类型 1：为查看  case or alcase 给了一个案例文件夹id 里边的xml都是  2：查看  casews 给了案例文件夹id 和 其中的具体 案例id  3：搜索 search==3
    :param text_id:    案例文件(.xml)id
    :param ids:        案例文件(.xml) ids
    :return:           案例文本数组
    """

    documents_files = os.listdir(documents_path)
    documents=[]

    if search==1: # 查看  case or alcase 给了一个案例文件夹id 里边的xml都是
        documents_files = os.listdir(documents_path)
        for xml_file in documents_files:
            # print(xml_file)
            if os.path.isdir(documents_path + "/" + xml_file):  # 判断是否是文件夹(xml_n文件夹)，是文件夹才打开
                search_doc_folders = os.listdir(documents_path + "/" + xml_file)
                for doc_folder in search_doc_folders:
                    if doc_folder == folder_id:
                        docs = os.listdir(documents_path + "/" + xml_file + "/" + doc_folder)  # 案例文件夹 中的具体xml案例
                        for doc in docs:
                            if doc.endswith(".xml"):
                                text = ET.parse(documents_path + "/" + xml_file + "/" + doc_folder + "/" + doc).find(
                                    "QW").attrib["oValue"]
                                documents.append(text)
                                print(doc, " Got it!")
    elif search==2:#查看  casews 给了案例文件夹id 和 其中的具体 案例id
        documents_files = os.listdir(documents_path)
        for xml_file in documents_files:
            # print(xml_file)
            if os.path.isdir(documents_path + "/" + xml_file):  # 判断是否是文件夹(xml_n文件夹)，是文件夹才打开
                search_doc_folders = os.listdir(documents_path + "/" + xml_file)
                for doc_folder in search_doc_folders:
                    if doc_folder == folder_id:
                        docs = os.listdir(documents_path + "/" + xml_file + "/" + doc_folder)  # 案例文件夹 中的具体xml案例
                        for doc in docs:
                            if doc.endswith(".xml") and doc.split(".")[0]==text_id:
                                text = ET.parse(documents_path + "/" + xml_file + "/" + doc_folder + "/" + doc).find(
                                    "QW").attrib["oValue"]
                                documents.append(text)
                                print(doc, " Got it!")
    else:#搜索 search==3
        for id in ids:
            documents_files = os.listdir(documents_path)
            for xml_file in documents_files:
                # print(xml_file)
                if os.path.isdir(documents_path + "/" + xml_file):  # 判断是否是文件夹(xml_n文件夹)，是文件夹才打开
                    search_doc_folders = os.listdir(documents_path + "/" + xml_file)
                    for doc_folder in search_doc_folders:
                        if doc_folder == id:
                            docs = os.listdir(documents_path + "/" + xml_file + "/" + doc_folder)  # 案例文件夹 中的具体xml案例
                            for doc in docs:
                                if doc.endswith(".xml"):
                                    text =ET.parse(documents_path + "/" + xml_file + "/" + doc_folder + "/" + doc).find("QW").attrib["oValue"]
                                    documents.append(text)
                                    print(doc," Got it!")
    return documents

json_path="five_user_log_sessions.json"




def read_json_data(json_path):
    users_sessions_data={}
    with open(json_path,'r',encoding="utf-8") as f:
        js_data=json.load(f)
        for user_id in js_data:
            user_data=js_data[user_id]
            sessions=[]
            for se in user_data:
                user_session=session()
                user_session.__dict__=se
                sessions.append(user_session)
            users_sessions_data[user_id]=sessions
    f.close()
    return users_sessions_data


if __name__=="__main__":
   # get_documents_from_sessions("SAT_Click.json",click_log_file_path_SAT_Click)
    get_documents_from_sessions("Click_Search.json",click_log_file_path_Click_Search)
    #get_documents_from_sessions()
    # users_sessions=parse_sessions_from_log(logsfilepath)
    # print(users_sessions["0808_58D7A68C84497105161B73E8FD955D60"][0].keystr)
    # with open("five_user_log_sessions.json",'r') as f:
    #     js=json.loads(f.read())
    #     users_sessions=json.loads(js)
    #
    #     print(users_sessions)

    #read_json_data(json_path)












