#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.common.config import user_stop_path_add, user_dic_path, W2V_VOCABULARY_PATH, SPORTS_KEYWORDS_REMOVE_PATH, \
    ALL_STAR_NAME_PATH, INDEX_SX_APP_CONTENT_PATH
from app.util.resources_net import resources_net

'''
预生成各种常量字典、集合
'''

USER_STOP = [w.strip() for w in open(user_stop_path_add, 'r', encoding='utf-8').readlines() if w.strip()]
USER_DIC = [w.strip() for w in open(user_dic_path, 'r', encoding='utf-8').readlines() if w.strip()]
# RESOURCES_DIC=[w.strip() for w in open(resources_dic_path,'r',encoding='utf-8').readlines() if w.strip()  ]
# RESOURCES_DIC=list(set(RESOURCES_DIC))
# RESOURCES=    RESOURCES_DIC    # [w.strip() for w in open(resources_path,'r',encoding='utf-8').readlines() if w.strip()]
# RESOURCES_VEDIO=[w.strip() for w in open(resources_vedio_path,'r',encoding='utf-8').readlines() if w.strip()  ]

# 生成关键字列表
RESOURCES_NET_KEYS = [w.strip() for w in resources_net.keys() if w.strip()]
RESOURCES_NET_KEYS_SET = set(RESOURCES_NET_KEYS)

# 词向量全部词集合
with open(W2V_VOCABULARY_PATH, 'r', encoding='utf-8') as fr:
    W2V_VOCABULARY_SET = set([w.strip() for w in fr.readlines() if w.strip()])

# 无意义体育类名词排除集合
with open(SPORTS_KEYWORDS_REMOVE_PATH, 'r', encoding='utf-8') as fr:
    SPORTS_KEYWORDS_REMOVE_SET = set([w.strip() for w in fr.readlines() if w.strip()])

# 明星类-明星名集合
with open(ALL_STAR_NAME_PATH, 'r', encoding='utf-8') as fr:
    ALL_STAR_NAME_SET = set([w.strip() for w in fr.readlines() if w.strip()])

# 内容类-内容及相关信息处理
with open(INDEX_SX_APP_CONTENT_PATH, 'r', encoding='utf-8') as fr:
    # 内容名集合
    INDEX_SX_APP_CONTENT_DICT = {}
    temp_list = []
    for line in fr.readlines():
        if line.strip():
            cont_name = line.strip().split()[0]
            cont_info = line.strip().split()[1:]
            temp_list.append(cont_name)
            INDEX_SX_APP_CONTENT_DICT[cont_name] = cont_info
    INDEX_SX_APP_CONTNAME_SET = set(temp_list)


if __name__ ==  "__main__":
    # 隔壁女生的日常 : ['1000', '刘俊峰', '吴晴|崔馨心|王佳慧|高杨|李云鹤|贠辰鑫|林川']
    # print(len(INDEX_SX_APP_CONTENT_DICT))
    # print(len(INDEX_SX_APP_CONTNAME_SET))
    str = '吴晴'
    print(str.split('|'))

