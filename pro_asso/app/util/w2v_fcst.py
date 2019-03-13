# -*- coding: utf-8 -*-
from gensim.models import Word2Vec
from gensim.similarities.index import AnnoyIndexer
import os
from app.common.config import model_path
from app.util.pre_model import W2V_VOCABULARY_SET

# 加载model目录下指定模型
path_to_model = os.path.join(model_path, 'word2vec')
model = Word2Vec.load(path_to_model)


# 从disk加载annoy indexer
path_to_indexer = os.path.join(model_path, 'annoy_indexer_100')
annoy_indexer_100 = AnnoyIndexer()
annoy_indexer_100.load(path_to_indexer)
annoy_indexer_100.model = model


# 使用模型计算输入词组
# 2018-03-08 使用indexer尝试解决cpu占用问题
def associate_words(words, cont_type, with_model=model, top_n=10):
    words = [w.strip() for w in words]
    res = {}
    tops = []
    if words is None or len(words) == 0:
        return res
    for i in range(len(words)):
        try:
            tops = (with_model.most_similar(positive=words[0:(len(words) - i)], topn=top_n, indexer=annoy_indexer_100))
            break
        except Exception as e:
            print('')
    if (len(tops)) == 0:
        return res
    if cont_type == 'sports':
        for w, sim in tops:
            if w not in words:
                res[w] = sim
    else:
        for w, sim in tops:
            if w in W2V_VOCABULARY_SET and w not in words:
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

