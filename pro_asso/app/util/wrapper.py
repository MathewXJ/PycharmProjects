from app.util.pre_model import RESOURCES_NET_KEYS_SET, RESORRCES_NET_SPORTS_SET
from app.util.resources_net import resources_net
from app.classify import predict


# 以关键词作为key，从常量字典中获取value
def _get_dic_list(kws):
    kws = [w.strip() for w in kws if w.strip() in RESOURCES_NET_KEYS_SET]
    if len(kws) == 0:
        return []
    out = []
    for k in kws:
        value = resources_net[k]
        if len(value) == 0:
            continue
        else:
            out.append(value)
    return out


def _get_words_dic(list1):
    kws = []
    # 汇总全部值
    for i in list1:
        kws += [w for w in i.keys()]
    # set()去除重复值，再转回list类型
    kws = list(set(kws))
    out = {}
    for w in kws:
        tp = []
        for j in list1:
            if w in j.keys():
                tp.append(float(j[w]))
        out[w] = sum(tp) / float(len(tp))
    # 排序后输出
    out = sorted(out.items(), key=lambda x: x[1], reverse=True)
    return out


def get_sort3(kws):
    dic_list = _get_dic_list(kws)
    return _get_words_dic(dic_list)


# 体育类结果筛选
def remove_notsports(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word in set(RESORRCES_NET_SPORTS_SET):
            res_dic[word] = sim
        else:
            if predict(word) == 'sports':
                res_dic[word] = sim
    return res_dic
