from app.util.pre_model import SPORTS_KEYWORDS_REMOVE_SET, INDEX_SX_APP_CONTNAME_SET, ALL_STAR_NAME_SET, \
    SPORT_MEMBERS_ALL_DIC, SPORT_TEAMS_ALL_DICT
from app.classify import predict
import time


# 筛除非体育词、无意义体育词
def remove_not_sports(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word not in SPORTS_KEYWORDS_REMOVE_SET and predict(word) == 'sports':
            res_dic[word] = sim
    return res_dic


# 筛除非咪咕内容
def remove_not_conts(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word in INDEX_SX_APP_CONTNAME_SET:
            res_dic[word] = sim
    return res_dic


# 筛除非搜索明星
def remove_not_people(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if word in ALL_STAR_NAME_SET:
            res_dic[word] = sim
    return res_dic


# 判断输入词是否是运动员名（包括绰号）
# 结合输入的联赛名和队名，防止重名影响
def is_sports_member(input_word, **kw):
    output_word = ''
    output_info = {}
    if kw:
        team_name = kw.get("teamName")
        league_name = kw.get("leagueName")
        for name, info in SPORT_MEMBERS_ALL_DIC.items():
            if team_name == info.get("teamName") or league_name == info.get("leagueName"):
                if input_word == name:
                    output_word = name
                    break
                else:
                    if input_word in info.get('alias'):
                        output_word = name
                        break
    else:
        if input_word in SPORT_MEMBERS_ALL_DIC:
            output_word = input_word
        else:
            for name, info in SPORT_MEMBERS_ALL_DIC.items():
                alias = info.get('alias')
                if input_word in alias:
                    output_word = name
                    break
    if output_word:
        output_info = SPORT_MEMBERS_ALL_DIC.get(output_word)
    return output_word, output_info


# 判断输入词是否是队名（包括绰号）
# 返回队名、相关信息
def is_sports_team(input_word, league_name=None):
    output_word = ''
    output_info = {}
    for key, info in SPORT_TEAMS_ALL_DICT.items():
        name = key.split('|')[1]
        alias = info.get('alias')
        alias.add(name)
        if not league_name:
            if input_word in alias:
                output_info = info
                if info.get("leagueType") == 'FOOTBALL':
                    output_word = name
                else:
                    output_word = info.get('WholeName')
                break
        else:
            if league_name == info.get('leagueName') and input_word in alias :
                output_info = info
                if info.get("leagueType") == 'FOOTBALL':
                    output_word = name
                else:
                    output_word = info.get('WholeName')
                break
    return output_word, output_info


# 筛除非体育人名结果
def remove_not_sports_member(input_dic, **kw):
    res_dic = {}
    for word, sim in input_dic.items():
        if is_sports_team(word, **kw):
            res_dic[is_sports_team(word)] = sim
    return res_dic


# 筛除非体育队名结果
def remove_not_sports_team(input_dic):
    res_dic = {}
    for word, sim in input_dic.items():
        if is_sports_member(word):
            res_dic[is_sports_member(word)[0]] = sim
    return res_dic


if __name__ == "__main__":
    word = '哈哈哈'
    print(len(SPORT_MEMBERS_ALL_DIC))
    time1 = time.time()
    rlt = is_sports_member(word, leagueName="NBA")
    time2 = time.time()
    print("Result: %s , it costs %s ms" % (rlt, (time2 - time1) * 1000))

    word = '江苏队'
    print(len(SPORT_TEAMS_ALL_DICT))
    time1 = time.time()
    rlt = is_sports_team(word,league_name='男排联赛')
    time2 = time.time()
    print("Result: %s , it costs %s ms" % (rlt, (time2 - time1) * 1000))
