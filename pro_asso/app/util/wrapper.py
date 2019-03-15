from app.util.pre_model import RESOURCES_NET_KEYS_SET, SPORTS_KEYWORDS_REMOVE_SET, INDEX_SX_APP_CONTENT_DICT, INDEX_SX_APP_CONTNAME_SET
from app.util.resources_net import resources_net
#from app.classify import predict
from app.util.constants import DATA_FIELD_CONTDISPLAYTYPE_DICT


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
# 去除无意义体育词
def remove_notsports(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word not in SPORTS_KEYWORDS_REMOVE_SET and predict(word) == 'sports':
            res_dic[word] = sim
    return res_dic


# 输入：内容名称
# 返回：该内容在搜索表中的关联信息
# 例如一级分类、主演、导演、主持、嘉宾
def get_rlt4content(cont_name):
    rlt = {}
    cont_info = INDEX_SX_APP_CONTENT_DICT.get(cont_name)
    # 一级分类编码转换
    if cont_info:
        cont_display_type = DATA_FIELD_CONTDISPLAYTYPE_DICT.get(cont_info[0])
        # 相关人员
        peoples = []
        for item in cont_info[1:]:
            peoples.extend(item.split('|'))
        if len(peoples) > 3:
            peoples = list(set(peoples[0:3]))
        if len(peoples) == 0:
            return rlt
        elif len(peoples) == 1:
            rlt[peoples[0]] = 1.0002
        else:
            rlt[peoples[0]] = 1.0002
        for people in peoples[1:]:
            rlt[people + cont_display_type] = 1.0001
    return rlt

def get_rlt4contents(kws):
    rlt = {}
    for w in kws:
        if w in INDEX_SX_APP_CONTNAME_SET:
            rlt.update(get_rlt4content(w))
    return rlt



if __name__ ==  "__main__":
    str = ['哈哈农夫']
    print(get_rlt4contents(str))