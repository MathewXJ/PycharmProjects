#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.common.config import user_stop_path_add, user_dic_path, W2V_VOCABULARY_PATH, SPORTS_KEYWORDS_REMOVE_PATH
from app.util.resources_net import resources_net

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
