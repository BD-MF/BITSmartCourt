import numpy as np
import pandas as pd

'''
   用户搜索session Bean  对应搜索日志里的一条log 具体参数如下：
'''
class session():

    def __init__(self,user_id,date,kind,keystr,case_type,view_id,view_folder,location_list,result_ids,contexts):
        """
        :param user_id(string): 用户id
        :param date(string):    时间
        :param kind(string):    类型：查看案件详情 案例研判检索分析 or 案例研判组合检索
        :param keystr(string):  用户搜索关键字
        :param case_type(string): 查看案件详情 属于用户点击事件 用于构建点击用户画像 为了区分 case 和 casews 和alcase
        :param view_id(string):   查看案件详情时 案件文件id
        :param view_folder(string):查看案件详情时 案件文件夹id
        :param location_list(int): 查看案件详情时 案件文件夹id/案件文件id 后紧随的 数字
        :param result_ids(list):  案例研判检索分析 or 案例研判组合检索 时的 result_ids
        :param contexts(list): 案件原文
        """
        self.user_id=user_id
        self.date=date
        self.kind=kind
        self.keystr=keystr
        self.result_ids=result_ids
        self.contexts=contexts
        self.case_type=case_type
        self.view_id=view_id
        self.location_list=location_list
        self.view_folder=view_folder



