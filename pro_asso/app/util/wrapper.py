from app.util.pre_model import RESOURCES_NET_KEYS_SET, INDEX_SX_APP_CONTENT_DICT, INDEX_SX_APP_CONTNAME_SET, \
    ALL_STAR_NAME_SET, SPORT_LEAGUES_ALL_DICT
from app.util.resources_net import resources_net
from app.util.douban_works_info import douban_works_info
from app.util.constants import DATA_FIELD_CONTDISPLAYTYPE_DICT
from app.util.w2v_fcst import associate_words
from app.util import constants
from app.util.remove_utils import remove_not_conts, remove_not_people, is_sports_member, is_sports_team, is_sports_league
import re, random


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


# 根据作品，获得相关作品及概率
# 来源：豆瓣数据
# 新增使用resources_net结果
def get_asso_contents(kws):
    kws = [w.strip() for w in kws if w.strip() in INDEX_SX_APP_CONTNAME_SET]
    if len(kws) == 0:
        return {}
    out = {}
    for cont_name in kws:
        value = douban_works_info.get(cont_name, None)
        if not value:
            continue
        else:
            asso_conts = [w.strip() for w in value.get("works_recommendations_10").split('|')]
            for i in range(len(asso_conts)):
                asso_cont = re.split('[ ·]', asso_conts[i])
                asso_cont = ''.join(asso_cont)
                out[asso_cont] = 1.1 - i * 0.001
    if not out:
        for k, v in (dict(get_sort3(kws))).items():
            out[k] = v
    return remove_not_conts(out)


# 根据人名，求相关的人名及概率
# 不超过三个
def get_asso_people(kws):
    kws = [w.strip() for w in kws if w.strip() in ALL_STAR_NAME_SET]
    if len(kws) == 0:
        return {}
    peoples = remove_not_people(associate_words(kws, "not-sports"))
    out = limit_dict_num(peoples, 3)
    return out


# 根据人名，求人名近期作品概率（处理接口starContent对象）
# 不超过五个
def get_star_contents(opus):
    if len(opus) == 0:
        return {}
    out = {}
    for i in range(len(opus)):
        cont_name = opus[i].get(constants.DATA_FIELD_CONTNAME)
        out[cont_name] = 1.1 - i * 0.01
    out = limit_dict_num(out, 4)
    return out


# 限制字典结果个数
def limit_dict_num(input_dict, num):
    out = {}
    keys = list(input_dict.keys())
    for k in keys[0:num]:
        out[k] = input_dict[k]
    return out


# 根据包含的联赛名，求相关信息及概率
# 新增参数项目名，若输入中不含联赛名且项目名非空，则返回该项目下任意赛事
def get_asso_sports_league(kws, media_proj=None):
    leagues_all = []
    if media_proj:
        league_type = constants.MEDIA_PROJ_DICT.get(media_proj)
        for name, info in SPORT_LEAGUES_ALL_DICT.items():
            if info.get("leagueType") == league_type:
                leagues_all.append(name)
    leagues = []
    for w in kws:
        if w.strip():
            tmp = is_sports_league(w.strip())
            if tmp[0]:
                leagues.append(tmp)
    out = {}
    if leagues: # 推荐关联出的联赛名
        for league in leagues:
            league_name = league[0]
            out[league_name] = 1.2
    else:  #无法提取联赛名，则推荐项目名相关联赛
        if leagues_all:
            for league_name in random.sample(leagues_all, len(leagues_all)//2 + 1):
                out[league_name] = 1.2
    return out


# 根据包含的球队名，求相关信息及概率
def get_asso_sports_team(kws, league_name=None):
    teams = []
    for w in kws:
        if w.strip():
            tmp = is_sports_team(w.strip(), league_name)
            if tmp[0]:
                teams.append(tmp)
    if not teams:
        return {}
    out = {}
    for team in teams:
        name = team[0]
        league_name = team[1].get('leagueName')
        key_members = []
        if team[1].get('key_members'):
            key_members = team[1].get('key_members').split('|')
        out[league_name] = 1.2
        out[name] = 1.1
        if len(key_members) > 0:
            for i in range(len(key_members)):
                out[key_members[i]] = 1.09 - i * 0.01
    return out


# 根据包含的人名，求相关信息及概率
def get_asso_sports_member(kws):
    members = []
    for w in kws:
        if w.strip():
            tmp = is_sports_member(w.strip())
            if tmp[0]:
                members.append(tmp)
    if not members:
        return {}
    out = {}
    team_names = []
    for member in members:
        name = member[0]
        league_name = member[1].get('leagueName')
        out[league_name] = 1.2
        out[name] = 1.1
        team_names.append(member[1].get('teamName'))
    out.update(get_asso_sports_team(team_names))
    return out


if __name__ == "__main__":
    str = ['北京', '梅开二度', 'VS', '上海','男排联赛']
    print(get_asso_sports_league(str))
    print(get_asso_sports_team(str))
    # print(get_asso_sports_member(str))

