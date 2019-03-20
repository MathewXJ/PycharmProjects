#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.common.config import user_stop_path_add, user_dic_path, W2V_VOCABULARY_PATH, SPORTS_KEYWORDS_REMOVE_PATH, \
    ALL_STAR_NAME_PATH, INDEX_SX_APP_CONTENT_PATH, VOCABULARY_PATH, SPORT_LEAGUES_ALL_PATH, SPORT_TEAMS_ALL_PATH, \
    SPORT_MEMBERS_ALL_PATH
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

# 词向量w2v关键词，解决模型报错问题
with open(VOCABULARY_PATH, 'r', encoding='utf-8') as fr:
    voc = fr.readlines()
    VOCABULARY_SET = set()
    for line in voc:
        if line.strip():
            VOCABULARY_SET.add(line.strip().split()[0].strip())


'''
2019-03-19
体育类字典初始化
包括CBA、NBA、五大联赛等联赛信息、队伍信息、队员信息
'''
# 球员名及相关信息
with open(SPORT_MEMBERS_ALL_PATH, 'r', encoding='utf-8') as fr:
    SPORT_MEMBERS_ALL_DIC = {}
    for line in fr.readlines():
        line = eval(line.strip())
        if line:
            member_info = {}
            name = line.get("name")
            leagueType = line.get("leagueType")
            member_info['leagueType'] = leagueType
            if leagueType == 'FOOTBALL':
                member_info['teamName'] = line.get("teamName")
                member_info['leagueName'] = line.get("leagueName")
            else:
                member_info['teamName'] = line.get("team")
                member_info['leagueName'] = leagueType
            # 别名-除alias字段外，还包括外国名的姓、去标点后的外国名
            alias_str = line.get("alias")
            alias = set()
            if alias_str:
                alias = set(alias_str.split('|'))
            if '·' in name:
                alias.add(name.split('·')[-1])
                alias.add(''.join(name.split('·')))
            if '-' in name:
                alias.add(name.split('-')[-1])
                alias.add(''.join(name.split('-')))
            member_info['alias'] = alias

            SPORT_MEMBERS_ALL_DIC[name] = member_info


# 球队名及相关信息
with open(SPORT_TEAMS_ALL_PATH, 'r', encoding='utf-8') as fr:
    SPORT_TEAMS_ALL_DICT = {}
    for line in fr.readlines():
        line = eval(line.strip())
        if line:
            team_info = {}
            team_name = line.get("name")
            # 别名-除alias字段外，队名加“队”字
            alias_str = line.get("alias")
            alias = set()
            if alias_str:
                alias = set(alias_str.split('|'))
            alias.add(team_name + "队")
            # 判断是否为NBA，NBA拼接city字段作为别名
            league_type = line.get("leagueType")
            if league_type == 'FOOTBALL':
                team_info['leagueName'] = line.get("leagueName")
            if league_type == 'CBA':
                team_info['leagueName'] = league_type
                team_info['WholeName'] = alias_str.split('|')[0]
            if league_type == 'NBA':
                team_info['leagueName'] = league_type
                team_info['WholeName'] = line.get("city") + team_name
                alias.add(line.get("city") + team_name)
                alias.add(line.get("city") + team_name + "队")

            team_info['leagueType'] = league_type
            team_info['alias'] = alias
            team_info['key_members'] = line.get('key_members')

            SPORT_TEAMS_ALL_DICT[team_name] = team_info


# 联赛名及相关信息
with open(SPORT_LEAGUES_ALL_PATH, 'r', encoding='utf-8') as fr:
    SPORT_LEAGUES_ALL_DICT = {}
    for line in fr.readlines():
        line = eval(line.strip())
        if line:
            league_info = {}
            league_name = line.get("name")
            SPORT_LEAGUES_ALL_DICT[league_name] = league_info



if __name__ == "__main__":
    print(SPORT_MEMBERS_ALL_DIC.get('乔尔·恩比德'))
    print(SPORT_TEAMS_ALL_DICT.get('同曦'))
    print(SPORT_TEAMS_ALL_DICT.get('火箭'))
    print(SPORT_TEAMS_ALL_DICT.get('拜仁慕尼黑'))
    print(SPORT_LEAGUES_ALL_DICT.keys())


