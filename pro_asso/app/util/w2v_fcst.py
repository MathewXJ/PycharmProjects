# -*- coding: utf-8 -*-
import time
from gensim.models import Word2Vec
import os
from app.common.config import model_path
from app.util.pre_model import RESOURCES_NET_KEYS_SET

# 加载model目录下指定模型
path_to_model = os.path.join(model_path, 'word2vec')
model = Word2Vec.load(path_to_model)


# 使用模型计算输入词组
def associate_words(words, cont_type, with_model=model, top_n=25):
    words = [w.strip() for w in words]
    res = {}
    tops = []
    if words is None or len(words) == 0:
        return res
    for i in range(len(words)):
        try:
            tops = (with_model.most_similar(positive=words[0:(len(words) - i)], topn=top_n))
            break
        except Exception as e:
            print('')
    if (len(tops)) == 0:
        return res
    if cont_type == 'sports':
        for w, sim in tops:
            if sim > 0.635:
                res[w] = sim
    else:
        for w, sim in tops:
            if w in RESOURCES_NET_KEYS_SET and sim > 0.635:
                res[w] = sim
    return res


if __name__ == "__main__":
    model.wv.save_word2vec_format("word2vec.dict", "vocabulary", binary=False)
    # words = ['火箭', '英语', '湖人', 'VS']
    # # words = ['回放', '森林狼', '18', '赛季', '135', 'NBA', '121', '奇才', '19', '常规赛']
    # # words = ['特种兵之深入敌后']
    # # words = ['领衔', '球员', '十佳', '英乙', '半场', '进球', '体育', '资讯', '吊射']
    # # words = ['上海队', '梅开二度', 'vs', '发球', '开局', '得分', '接连', '直接', '北京', '上海']
    # print(associate_words(words,'sports'))

