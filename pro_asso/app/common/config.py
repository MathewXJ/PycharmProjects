#!/usr/bin/python
# -*- coding: UTF-8 -*-

# underlying used by LOG_LEVEL
import logging
import os
from os.path import join, dirname, abspath
from configparser import ConfigParser

# 关于路径！尽可能使用os.path.join以排除系统差异

# 获取项目根路径
def getProjectDir():
    config_path = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.split(os.path.split(config_path)[0])[0]
    return project_dir


# 拼接config目录路径
config_path = os.path.join(getProjectDir(), 'config')
config_dic_path = os.path.join(config_path, 'dic')

# 拼接配置项路径
user_stop_path=os.path.join(config_dic_path, 'user_stop')
user_dic_path=os.path.join(config_dic_path, 'user_dic_shehuang')
user_stop_path_add= os.path.join(config_dic_path, 'user_stop_add')
resources_path=os.path.join(config_path, 'resources_dic')
resources_dic_path=os.path.join(config_path, 'resources_dic')
resources_vedio_path=os.path.join(config_path, 'mediaVideoName2')


# 拼接model目录路径
model_path = os.path.join(getProjectDir(), 'model')

# 用户词典/本地缓存目录路径
model_user_dict_path = os.path.join(model_path, 'user_dicts')


#weight_acs_acs=1.30
#weight_acs_vedio=1.30

weight_base=1.20
weight_vedio=1.29


# 读取配置文件
cp = ConfigParser()
app_path = dirname(dirname(abspath(__file__)))
conf_file_path = join(dirname(app_path), 'config', 'config.conf')
cp.read(filenames=conf_file_path, encoding='utf-8')


# 端口号配置
PRO_ASSO_PORT = eval(cp['webapp.settings']['PRO_ASSO_PORT'])

# 是否返回预测概率
RETURN_PROB = eval(cp['common.settings']['RETURN_PROB'])

# 日志路径, level, 文件名
LOG_PATH = os.path.join(getProjectDir(), cp['log.settings']['LOG_PATH'])
LOG_LEVEL = eval(cp['log.settings']['LOG_LEVEL'])
LOG_FILE_NAME = cp['log.settings']['LOG_FILE_NAME']

# 搜索词分类模型设置
MODEL_NAME = eval(cp['model.settings']['MODEL_NAME'])
MODEL_FILE_PATH = join(model_path, MODEL_NAME)

# label prefix
LABEL_PREFIX = eval(cp['model.settings']['LABEL_PREFIX'])

# jieba分词-用户字典-体育类使用
USER_DIC_NAME = eval(cp['model.settings']['USER_DIC_NAME'])
USER_DIC_PATH = join(model_user_dict_path, USER_DIC_NAME)

# jieba分词-用户字典-from resources_net
W2V_VOCABULARY_PATH = join(model_user_dict_path, 'w2v_vocabulary')

# 体育类要排除的词
SPORTS_KEYWORDS_REMOVE_PATH = join(model_user_dict_path, 'sports_keywords_remove')

# 明星类-明星名
ALL_STAR_NAME_PATH = join(model_user_dict_path, 'all_star_name')

# 内容类-内容及相关信息-from table:index_sx_app_content-2019.03.15 11：00：00
INDEX_SX_APP_CONTENT_PATH = join(model_user_dict_path, 'index_sx_app_content')
