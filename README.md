# BITSmartCourt
BIT Smart Court Project of School of Computer Science
Smart Court目前包括LDA文件夹，LDA文件夹内目前有四个py文件 session用是户搜索session Bean  对应搜索日志里的一条log session 
           num_topics.py 用来决定 LDA模型的最优主题数
           lda.py 为ntopics 来构建LDA
           data_process 为数据处理部分 包括从目前五个用户的搜索日志中 提取一条条的session 并在 xml日志中搜索相应xml文件并解析其具体参数 、中文分词、字符串清洗等
           
           生成的大的json ：five_user_log_sessions.json 是找到的五个用户的搜索日志 生成的 搜索记录 其形式为json, 具体包括五个大部分 对应五个人
           {user_id1 :[session1,session2,....];
            user_id2:[session1,session2,....];
            user_id3 :[session1,session2,....];
            user_id4:[session1,session2,....];
            user_id5 :[session1,session2,....]
           }
           
           
           
           每个session bean ,用于构建后期各用户画像 具体为：

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
           
