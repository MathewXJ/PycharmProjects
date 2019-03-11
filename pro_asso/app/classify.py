# coding=utf-8
import fasttext
# windows版本fasttext大坑
# import fastText.FastText as fasttext
import jieba_fast as jieba
import numpy as np
from app.common.config import MODEL_FILE_PATH, USER_DIC_PATH, LABEL_PREFIX, RETURN_PROB

jieba.load_userdict(USER_DIC_PATH)

# load训练好的模型
classifier = fasttext.load_model(MODEL_FILE_PATH, label_prefix=LABEL_PREFIX)

with open(USER_DIC_PATH, 'r', encoding='utf-8') as fr:
    KEYWORDS = set([line.strip() for line in fr.readlines() if line.strip()])

SYM = r'‘’?<>[]{}\|,.;\"!@#$%^&*()~`·。，、！～…=？/；（）『』【】“”×￥'
SUBSTR = ['&nbsp;', '&ldquo;', '&rdquo;', '&quot;', '&middot;']


def rinse_string(sens):
    cont = sens
    # 去子串
    for sub in SUBSTR:
        cont = cont.replace(sub, '')

    # 去标点符号
    out_tab = ''.join(np.repeat(' ', len(SYM)))
    tran_tab = cont.maketrans(SYM, out_tab)
    cont = cont.translate(tran_tab).replace(' ', '')

    # 大写转小写
    cont = cont.lower()
    return cont


# 分词，返回List
def cut2list(sentence):
    seg_list = [w.strip() for w in jieba.cut(sentence) if w.strip()]
    return seg_list


def preprocess_data(content):
    # cont_rinse = rinse_string(content)
    cont_seg = cut2list(content)
    if len(cont_seg) == 0:
        print('cut2list return empty : {}'.format(content))
        return None
    cont_seg_str = ' '.join(cont_seg)
    return cont_seg_str


def generate_result(label, prob=0.0):
    if not RETURN_PROB:
        return label
    else:
        return {label: prob}


def predict(line):
    cont_rinse = rinse_string(line.strip())
    # 匹配到关键词
    if cont_rinse in KEYWORDS:
        return generate_result('sports', prob=1.0)

    # 送入模型预测
    cont_seg_str = preprocess_data(cont_rinse)
    if not cont_seg_str:
        return generate_result('uncertain', prob=1.0)
    # label_prob格式：[[('porn', 0.978516), ('normal', 0.0117188), ...]]
    label_prob = classifier.predict_proba([cont_seg_str.strip()])
    label_prob = label_prob[0][0]
    return generate_result(label_prob[0], prob=float(label_prob[1]))


# if __name__ == "__main__":
#     RESOURCES_NET_KEYS = [w.strip() for w in resources_net.keys() if w.strip()]
#     sports_words = []
#     for w in RESOURCES_NET_KEYS:
#         if predict(w) == 'sports':
#             sports_words.append(w)
#     with open('sports_words.py', 'w') as f:
#         f.write('sports_words = [' + '\n')
#         for i in range(len(sports_words)):
#             if i == len(sports_words) - 1:
#                 f.write('\'' + sports_words[i] + r"'" + '\n')
#             else:
#                 f.write('\'' + sports_words[i] + r"'," + '\n')
#         f.write(']')
