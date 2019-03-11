# from app.util import w2v_fcst as wf, seg_jieba_extend as sje
# from app.util.wrapper import get_sort3
# import jieba
# from jieba import analyse
# from app.util.pre_model import RESOURCES_NET_KEYS
# import time


str = r'上海vs北京：上海队开局接连发球直接得分，梅开二度'
# t1 = time.time()
# kws = [word for word in analyse.extract_tags(str, topK=10)]
# t2 = time.time()
# print(kws)
# print((t2-t1)*1000)
# res_dic = wf.associate_words(kws)
# rlt = [key for key in res_dic.keys() if key in RESOURCES_NET_KEYS]
# print(res_dic)
# print(rlt)

# kws = sje.keywords_extract(str)
res_dic = {'破门': 1.0737362742424013}
dic2 = {'辽宁队': 0.8129979372024536, '进球': 0.8284926414489746, '破门': 0.0737362742424013, '扳平': 0.8040685653686523}
res_dic.update(dic2)
print(res_dic)
