import gensim
import time
from gensim.similarities.index import AnnoyIndexer
from gensim.models import Word2Vec


# 加载word2vec模型
path_to_model = '../model/word2vec'
model = Word2Vec.load(path_to_model)

# # 创建annoy indexer并关联word2vec模型
# # t0 = time.time()
# # annoy_indexer_100 = AnnoyIndexer(model, 300)
# # t1 = time.time()
# # print("Create AnnoyIndexer: {}ms".format(1000*(t1-t0)))
# #
# # # 保存annoy indexer到disk
# # annoy_indexer_100.save('annoy_indexer_100')
# # t2 = time.time()
# # print("Save AnnoyIndexer to File : {}ms".format(1000*(t2-t1)))

# 从disk加载annoy indexer
t1 = time.time()
annoy_indexer_100 = AnnoyIndexer()
annoy_indexer_100.load('annoy_indexer_100')
annoy_indexer_100.model = model
t2 = time.time()
print("从disk加载annoy indexer : {}ms".format(1000*(t2-t1)))


# 计算相似度
pos1 = ['上海队', '梅开二度', 'vs', '发球', '开局', '得分', '接连', '直接', '北京', '上海']
pos2 = ['火箭', '英语', 'NBA', 'VS']
pos3 = ['回放', '森林狼', '18', '赛季', '135', 'NBA', '121', '奇才', '19', '常规赛']
pos4 = ['威斯布鲁克', '雷霆队', '凯尔特人队']
pos5 = ['领衔', '球员', '十佳', '英超', '半场', '进球', '体育', '资讯', '吊射']
t2 = time.time()
print(model.most_similar(positive=pos1, topn=25, indexer=annoy_indexer_100))
t3 = time.time()
print("First Query : {}ms".format(1000*(t3-t2)))
print(model.most_similar(positive=pos2, topn=6, indexer=annoy_indexer_100))
print(model.most_similar(positive=pos3, topn=6, indexer=annoy_indexer_100))
print(model.most_similar(positive=pos4, topn=6, indexer=annoy_indexer_100))
print(model.most_similar(positive=pos5, topn=6, indexer=annoy_indexer_100))
t4 = time.time()
print("Query 4 times : {}ms".format(1000*(t4-t3)))

