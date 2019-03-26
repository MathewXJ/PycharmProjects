#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections
from app.util.wrapper import get_sort3, get_asso_contents, get_asso_people, limit_people_num, get_asso_sports_league, \
    get_asso_sports_team, get_asso_sports_member
from app.util import w2v_fcst as wf, seg_jieba_extend as sje
from app.util import constants
from app.classify import predict
import time
from app.common.utils import get_param_value
from app.util.remove_utils import remove_not_sports, remove_not_conts, remove_not_people


# 求关联词结果
def get_asso_rlt(cont):
    # 预测输入是否为体育类
    cont_type = predict(cont)
    res_dic = {}
    if cont_type == 'sports':
        res_dic = get_asso_rlt_sports(cont)
    else:
        res_dic = get_asso_rlt_not_sports(cont)
    return res_dic


# 非体育类
# 规则：若含内容，推荐相关内容；若含人名，推荐相关人名（限制三个）
# 先提取《》中内容，并不再使用常量字典的结果
def get_asso_rlt_not_sports(cont):
    res_dic = {}
    # 提取《》中内容
    cont_names = sje.get_book_title(cont)[0]
    cont = sje.get_book_title(cont)[1]

    # 提取关键词jieba+flashtext
    kws = sje.keywords_extract(cont)
    kws.extend(sje.keywords_analyse(cont))
    kws = list(set(kws))
    kws_new = sje.distinct_words(kws)

    # 求内容相关
    if cont_names:
        res_dic_contents = get_asso_contents(cont_names)
    else:
        res_dic_contents = get_asso_contents(kws_new)

    # 求人名相关
    res_dic_people = get_asso_people(kws_new)

    # 合并结果
    res_dic_contents.update(limit_people_num(res_dic_people, 3))
    res_dic.update(res_dic_contents)

    return res_dic


# 体育类
def get_asso_rlt_sports(cont):
    res_dic = {}
    # 直接提取输入中的关键字列表
    kws = sje.keywords_extract(cont)

    kws_extend = kws[:]
    kws_extend.extend(sje.keywords_analyse(cont))
    kws_extend = list(set(kws_extend))
    kws_new = sje.distinct_words(kws_extend)

    # 提取关键字中联赛名及相关信息
    res_dic_league = get_asso_sports_league(kws_new)
    res_dic.update(res_dic_league)

    # 提取关键字中队名及相关信息
    # 根据是否获取到联赛名进行不同处理
    league_names = list(res_dic_league.keys())
    res_dic_team = {}
    if len(league_names) > 0:
        for league_name in league_names:
            res_dic_team.update(get_asso_sports_team(kws_new, league_name))
    else:
        res_dic_team.update(get_asso_sports_team(kws_new))
    res_dic.update(res_dic_team)

    # 提取关键字中运动员名及相关信息
    res_dic.update(get_asso_sports_member(kws_new))

    # 数量不够再使用模型预测
    res_dic_predict = {}
    if len(res_dic) < 3:
        kws_new = [w.strip() for w in kws_new if predict(w) == 'sports']
        for k, v in (dict(get_sort3(kws_new))).items():
            res_dic_predict[k] = v
        res_dic_predict.update(wf.associate_words(kws_new, 'sports'))
        res_dic_predict = remove_not_sports(res_dic_predict)
    res_dic.update(res_dic_predict)

    #去小写例如nba，只保留NBA;
    res_dic_last = {}
    for key, value in res_dic.items():
        key = key.upper()
        res_dic_last[key] = value
    return res_dic_last


# def get_asso_rlt_sports(cont):
#     cont_type = 'sports'
#     res_dic = {}
#
#     # 直接提取输入中的关键字列表
#     time1 = time.time()
#     kws = sje.keywords_extract(cont)
#     # 取常量字典中关键词对应结果
#     for k, v in (dict(get_sort3(kws))).items():
#         res_dic[k] = v


#         # 取常量字典中内容名对应结果
#     for k, v in (dict(get_sort3(cont_name))).items():
#         res_dic[k] = v
#     # 过滤内容结果
#     res_dic_contents = remove_not_conts(res_dic)
#     # 过滤人名结果
#     res_dic_people = remove_not_people(res_dic)


#     time2 = time.time()
#     # print("(1) keywords extract result : {},  costs : {} ms".format(res_dic, (time2 - time1) * 1000))
#
#     if cont_type == 'sports':
#         res_dic = remove_not_sports(res_dic)
#
#     # 若结果小于5，则加入jieba分词结果并使用模型计算
#     if len(res_dic) < 5:
#         time3 = time.time()
#         kws_extend = kws[:]
#         kws_extend.extend(sje.keywords_analyse(cont))
#         kws_extend = list(set(kws_extend))
#         kws_new = sje.distinct_words(kws_extend)
#         if cont_type == 'sports':
#             kws_new = [w.strip() for w in kws_new if predict(w) == 'sports']
#         time4 = time.time()
#         # print("(2) keywords analyse result : {},  costs : {} ms".format(res_dic, (time4 - time3) * 1000))
#         # 无包含关系，则扩展原结果
#         if kws_new == kws or kws_new == kws_extend:
#             res_dic.update(wf.associate_words(kws_new, cont_type))
#         # 有包含关系，则忽略原结果
#         else:
#             res_dic = wf.associate_words(kws_new, cont_type)
#         time5 = time.time()
#         # print("(3) associate words result : {},  costs : {} ms".format(res_dic, (time5 - time4) * 1000))
#
#     return res_dic


# 求关联词结果-json输入
def get_asso_rlt_json(req_data):
    cont = get_param_value(constants.DATA_FIELD_CONT, req_data)
    cont_name = get_param_value(constants.DATA_FIELD_CONTNAME, req_data)
    cont_display_type = get_param_value(constants.DATA_FIELD_CONTDISPLAYTYPE, req_data)
    # 预测输入是否为体育类
    cont_type = predict(cont)
    # cont_type = 'sports'
    res_dic = {}
    # 获取输入中的关键字列表
    kws = sje.keywords_extract(cont)
    for k, v in (dict(get_sort3(kws))).items():
        res_dic[k] = v

    if cont_type == 'sports':
        res_dic = remove_not_sports(res_dic)

    # 若结果小于5，则加入jieba分词结果并使用模型计算
    if len(res_dic) < 5:
        kws_extend = kws[:]
        kws_extend.extend(sje.keywords_analyse(cont))
        kws_extend = list(set(kws_extend))
        kws_new = sje.distinct_words(kws_extend)
        # 无包含关系，则扩展原结果
        if kws_new == kws or kws_new == kws_extend:
            res_dic.update(wf.associate_words(kws_new, cont_type))
        # 有包含关系，则忽略原结果
        else:
            res_dic = wf.associate_words(kws_new, cont_type)
    return res_dic


if __name__ == "__main__":
    # print(get_asso_rlt('CBA常规赛第6轮：上海队 蔡亮开球分给弗雷戴特，插羽破天骄，三分扳平比分'))
    # print(get_asso_rlt('18/19赛季NBA常规赛全场回放：森林狼121:135奇才'))
    print(get_asso_rlt('特种兵之深入敌后'))
