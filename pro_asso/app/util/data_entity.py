from app.common.utils import get_param_value


# 搜索传入内容封装
class InputData(object):
    # 必传字段
    def __init__(self, cont, program_id, cont_name, cont_display_type):
        # 搜索词
        self.cont = cont
        # 节目ID
        self.program_id = program_id
        # 视频名称x
        self.cont_name = cont_name
        # 一级分类
        self.cont_display_type = cont_display_type

    # JSON转对象
    def get_json_data(self, json_data):
        self.cont = get_param_value('cont', json_data)
        self.program_id = get_param_value('programId', json_data)
        self.cont_name = get_param_value('contName', json_data)
        self.cont_display_type = get_param_value('contDisplayType', json_data)
        self.star_content = get_param_value('starContent', json_data)

