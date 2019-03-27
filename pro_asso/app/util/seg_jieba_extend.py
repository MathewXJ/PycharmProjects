# -*- coding: utf-8 -*-
__author__ = 'xujian'

import jieba.posseg as pseg
from jieba import analyse, load_userdict
from app.util.pre_model import RESOURCES_NET_KEYS, USER_STOP, INDEX_SX_APP_CONTNAME_SET
from flashtext import KeywordProcessor
from app.common.config import W2V_VOCABULARY_PATH, ALL_STAR_NAME_PATH, INDEX_SX_APP_CONTENT_NAME_PATH, USER_DIC_PATH
import re

# 导入关键字
resources_net_processor = KeywordProcessor()
resources_net_processor.add_keywords_from_list(RESOURCES_NET_KEYS)
resources_net_processor.add_keywords_from_list(list(INDEX_SX_APP_CONTNAME_SET))
resources_net_processor.add_keyword_from_file(USER_DIC_PATH)

# 导入用户字典
load_userdict(W2V_VOCABULARY_PATH)
load_userdict(ALL_STAR_NAME_PATH)
load_userdict(INDEX_SX_APP_CONTENT_NAME_PATH)
load_userdict(USER_DIC_PATH)


# 分词，词性标注，词和词性构成一个元组
def postagger(sentence):
    pos_data = pseg.cut(sentence)
    pos_list = []
    for w in pos_data:
        if w.word.strip() == '': continue
        pos_list.append((w.word, sym2name(w.flag)))
    # print pos_list[:]
    return pos_list


def get_key_words2_tp(cont, topn=10):
    return [cont.strip()]


# 2019-02-26更新，拆分关键词获取方法，保留flashtext优先，不影响性能
# flashtext提取关键字列表
def keywords_extract(content):
    # 快速提取已有关键字
    kws = resources_net_processor.extract_keywords(content)
    return distinct_words(kws)


# 获取jieba分词结果，供模型计算用
def keywords_analyse(content, top_n=30):
    # 使用jieba重新分词（不做key限制）
    kws = [w for w in analyse.extract_tags(content, topK=top_n)]
    return distinct_words(kws)


# 去除包含关系的词
def distinct_words(words):
    rlt = []
    # 去除包含关系的词
    for i, w in enumerate(words):
        str_left_combine = ''.join(words[0:i] + words[(i + 1):len(words)])
        # 例如“[大江大河,大江,大河] ['花不弃', '小女']这两种情况很特殊，再加条件限制”
        if w in str_left_combine:
            if w != str_left_combine:
                continue
            else:
                rlt.append(w)
        else:
            rlt.append(w)
    return rlt


# 提取《》内的内容
# 返回(r1,r2) r1为书名号中内容组成的列表，r2其它字符串拼接后的字符串
# 《爸爸去哪儿2》此种节目名并不规范，需要去除数字2
def get_book_title(input_str):
    pattern = r'《.*?》'
    tmp_list = [w.strip('《》') for w in re.findall(pattern, input_str)]
    cont_list = [''.join(re.split(r'\d+$', w)) for w in tmp_list]
    output_str = ''.join(re.split(pattern, input_str))
    return cont_list, output_str



# print( [w for w in  analyse.extract_tags('大江大河') if w in RESOURCES_NET_KEYS ]   )
# print('大江大河'  in RESOURCES_NET_KEYS)
# 去除停用词
def del_stopwords(seg_sent):
    stopwords = USER_STOP  # 读取停用词表
    new_sent = []  # 去除停用词后的句子
    for word in seg_sent:
        if word in stopwords:
            continue
        else:
            new_sent.append(word)
    return new_sent


def del_stopwords2(seg_sent):
    stopwords = USER_STOP  # 读取停用词表
    new_sent = []  # 去除停用词后的句子
    for word in seg_sent:
        if word[0].strip() in stopwords:
            continue
        else:
            new_sent.append(word)
    return new_sent


def sym2name(sym):
    res = ''
    if sym == 'Ag':
        res = '形容词性语素'
    elif sym == 'a':
        res = '形容词'
    elif sym == 'ad':
        res = '状语形容词'
    elif sym == 'an':
        res = '名词功能形容词'
    elif sym == 'b':
        res = '区别词'

    elif sym == 'c':
        res = '连词'
    elif sym == 'dg':
        res = '副词性语素'
    elif sym == 'd':
        res = '副词'
    elif sym == 'e':
        res = '叹词'
    elif sym == 'f':
        res = '方位词'

    elif sym == 'g':
        res = '语素'
    elif sym == 'h':
        res = '前接成分'
    elif sym == 'i':
        res = '成语'
    elif sym == 'j':
        res = '简称略语'
    elif sym == 'k':
        res = '后接成分'

    elif sym == 'l':
        res = '习用语'
    elif sym == 'm':
        res = '数词'
    elif sym == 'Ng':
        res = '名词性语素'
    elif sym == 'n':
        res = '名词'
    elif sym == 'nr':
        res = '人名'

    elif sym == 'ns':
        res = '地名'
    elif sym == 'nt':
        res = '机构团体'
    elif sym == 'nz':
        res = '其他专名'
    elif sym == 'o':
        res = '拟声词'
    elif sym == 'p':
        res = '介词'

    elif sym == 'q':
        res = '量词'
    elif sym == 'r':
        res = '代词'
    elif sym == 's':
        res = '处所词'
    elif sym == 'tg':
        res = '时间词性语素'
    elif sym == 't':
        res = '时间词'

    elif sym == 'u':
        res = '助词'
    elif sym == 'vg':
        res = '动词性语素'
    elif sym == 'v':
        res = '动词'
    elif sym == 'vd':
        res = '作状语的动词'
    elif sym == 'vn':
        res = '名动词'

    elif sym == 'w':
        res = '标点符号'
    elif sym == 'x':
        res = '非语素字'
    elif sym == 'y':
        res = '语气词'
    elif sym == 'z':
        res = '状态词'
    elif sym == 'un':
        res = '未知词'
    else:
        res = sym
    return res


def read_lines(file_path):
    with open(file_path, 'r') as f:
        return f.readlines()


# 获取六种权值的词，根据要求返回list，这个函数是为了配合Django的views下的函数使用
def read_quanzhi(request):
    result_dict = []
    if request == "one":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/most.txt")
    elif request == "two":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/very.txt")
    elif request == "three":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/more.txt")
    elif request == "four":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/ish.txt")
    elif request == "five":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/insufficiently.txt")
    elif request == "six":
        result_dict = read_lines("f://emotion/mysite/Sentiment_dict/degree_dict/inverse.txt")
    else:
        pass
    return result_dict


if __name__ == "__main__":
    cont = 'CBA常规赛第6轮：上海队 蔡亮开球分给弗雷戴特，插羽破天骄，三分扳平比分'
    # cont = '18/19赛季NBA常规赛全场回放：森林狼121:
    cont = '特种兵之深入敌后'
    # cont = '（体育资讯）英乙球员半场吊射领衔周十佳进球'
    #cont = '《声临其境2》“雪姨”王琳陕西话俄语秒切换'
    #cont = '吴京《战狼2》超燃高能情节'
    cont = '18/19赛季NBA常规赛全场回放：马刺112:105独行侠（20190313）'
    cont = '小女花不弃:林依晨张彬彬上演虐恋情深，莲花夫妇锁了！'
    cont = '妻子的浪漫旅行2'
    cont = '中国男排超级联赛，上海VS北京'
    cont = '18/19赛季CBA常规赛第46轮全场回放：上海124：89福建（荆超、陈正昊）'
    #cont = '上海VS北京,上海开局接连发球直接得分，梅开二度'
    cont = '《冷枪手》特工队血腥护宝再掀谍战风云'
    cont = '盐城响水“3·21”事故：昨夜今晨消防员全力搜救被困人员'
    cont = '杨幂杨幂,湖南平江站'
    content_names = get_book_title(cont)[0]
    cont_left = get_book_title(cont)[1]
    print(content_names)
    print([w for w in analyse.extract_tags(cont, topK=30)])
    kws = keywords_extract(cont)
    kws_extend = kws[:]
    print('原提取结果：', kws)
    kws_extend.extend(keywords_analyse(cont))
    kws_extend = list(set(kws_extend))
    kws_new = distinct_words(kws_extend)
    print('扩展并去重后提取结果：', kws_extend)
    print('去包含结果：', kws_new)