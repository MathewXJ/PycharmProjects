# coding=utf-8
import fasttext
import jieba_fast as jieba
import numpy as np
from app.common.utils import dbc2sbc
from app.common.config import MODEL_FILE_PATH, USER_DIC_PATH, LABEL_PREFIX, RETURN_PROB, ALL_STAR_NAME_PATH, \
    INDEX_SX_APP_CONTENT_NAME_PATH

jieba.load_userdict(USER_DIC_PATH)
jieba.load_userdict(ALL_STAR_NAME_PATH)
jieba.load_userdict(INDEX_SX_APP_CONTENT_NAME_PATH)

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
    # 全角转半角
    cont = dbc2sbc(cont.strip())
    # 大写转小写
    cont = cont.lower()
    return cont


# 分词，返回List
def cut2list(sentence):
    seg_list = [w.strip() for w in jieba.cut(sentence) if w.strip()]
    return seg_list


def preprocess_data(content):
    # cont_rinse = rinse_string(content)
    cont_seg_list = cut2list(content)
    if len(cont_seg_list) == 0:
        print('cut2list return empty : {}'.format(content))
        return None
    # cont_seg_str = ' '.join(cont_seg)
    return cont_seg_list


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

    # 没有匹配到关键词，则送入模型预测
    cont_seg_list = preprocess_data(cont_rinse)
    if not cont_seg_list:
        return generate_result('uncertain', prob=1.0)
    # label_prob格式：[[('porn', 0.978516), ('normal', 0.0117188), ...]]
    label_prob = classifier.predict_proba([' '.join(cont_seg_list).strip()])
    label_prob = label_prob[0][0]
    # 整体预测为non-sports，但是每个分词都是体育类的，则强制返回sports
    if label_prob[0] != 'sports':
        all_sports_kw = True
        for w in cont_seg_list:
            if w not in KEYWORDS:
                all_sports_kw = False
                break
        if all_sports_kw:
            return generate_result('sports', prob=1.0)

    return generate_result(label_prob[0], prob=float(label_prob[1]))
