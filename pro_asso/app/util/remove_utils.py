from app.util.pre_model import SPORTS_KEYWORDS_REMOVE_SET, INDEX_SX_APP_CONTNAME_SET, ALL_STAR_NAME_SET
from app.classify import predict

# 体育类结果筛选
# 去除无意义体育词
def remove_notsports(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word not in SPORTS_KEYWORDS_REMOVE_SET and predict(word) == 'sports':
            res_dic[word] = sim
    return res_dic



def remove_not_conts(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word in INDEX_SX_APP_CONTNAME_SET:
            res_dic[word] = sim
    return res_dic


def remove_not_people(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word in ALL_STAR_NAME_SET:
            res_dic[word] = sim
    return res_dic