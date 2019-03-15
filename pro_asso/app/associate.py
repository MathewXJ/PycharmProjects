#!/usr/bin/python
# -*- coding: UTF-8 -*-
import collections
from app.util.wrapper import get_sort3, remove_notsports, get_rlt4contents
from app.util import w2v_fcst as wf, seg_jieba_extend as sje
from app.util import constants
from app.classify import predict
import time
from app.common.utils import get_param_value

# 求关联词结果
def get_asso_rlt(cont):
    # 预测输入是否为体育类
    cont_type = predict(cont)
    #cont_type = 'sports'
    res_dic = {}

    # 直接提前输入中的关键字列表
    time1 = time.time()
    kws = sje.keywords_extract(cont)
    # 取常量字典中关键词对应结果
    for k, v in (dict(get_sort3(kws))).items():
        res_dic[k] = v
    # 取搜索内容表中内容名对应结果
    res_dic.update(get_rlt4contents(kws))
    time2 = time.time()
    print("(1) keywords extract result : {},  costs : {} ms".format(res_dic, (time2 - time1) * 1000))

    if cont_type == 'sports':
        res_dic = remove_notsports(res_dic)

    # 若结果小于6，则加入jieba分词结果并使用模型计算
    if len(res_dic) < 6:
        time3 = time.time()
        kws_extend = kws[:]
        kws_extend.extend(sje.keywords_analyse(cont))
        kws_extend = list(set(kws_extend))
        kws_new = sje.distinct_words(kws_extend)
        if cont_type == 'sports':
            kws_new = [w.strip() for w in kws_new if predict(w) == 'sports']
        print(kws_new)
        time4 = time.time()
        print("(2) keywords analyse result : {},  costs : {} ms".format(res_dic, (time4 - time3) * 1000))
        # 无包含关系，则扩展原结果
        if kws_new == kws or kws_new == kws_extend:
            res_dic.update(wf.associate_words(kws_new, cont_type))
        # 有包含关系，则忽略原结果
        else:
            res_dic = wf.associate_words(kws_new, cont_type)
        time5 = time.time()
        print("(3) associate words result : {},  costs : {} ms".format(res_dic, (time5 - time4) * 1000))

    return res_dic


# 求关联词结果-json输入
def get_asso_rlt_new(req_data):
    cont = get_param_value(constants.DATA_FIELD_CONT, req_data)
    cont_name = get_param_value(constants.DATA_FIELD_CONTNAME, req_data)
    cont_display_type = get_param_value(constants.DATA_FIELD_CONTDISPLAYTYPE, req_data)
    # 预测输入是否为体育类
    cont_type = predict(cont)
    #cont_type = 'sports'
    res_dic = {}
    # 获取输入中的关键字列表
    kws = sje.keywords_extract(cont)
    for k, v in (dict(get_sort3(kws))).items():
        res_dic[k] = v

    if cont_type == 'sports':
        res_dic = remove_notsports(res_dic)

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
    #print(get_asso_rlt('CBA常规赛第6轮：上海队 蔡亮开球分给弗雷戴特，插羽破天骄，三分扳平比分'))
    #print(get_asso_rlt('18/19赛季NBA常规赛全场回放：森林狼121:135奇才'))
    print(get_asso_rlt('特种兵之深入敌后'))