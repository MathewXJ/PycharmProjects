import os
import logging

from app.common.safe_file_handler import SafeFileHandler
from app.common.config import LOG_PATH, LOG_LEVEL, LOG_FILE_NAME


def init_log_settings(logger, log_file=LOG_FILE_NAME):
    """
    初始化日志设置
    :param logger:
    :param log_file:
    :return:
    """
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    handler = SafeFileHandler(filename=os.path.join(LOG_PATH, log_file), encoding='utf-8')
    handler.setLevel(LOG_LEVEL)
    logging_format = logging.Formatter('%(asctime)s - %(levelname)s - %(process)d - %(thread)d -'
                                       '%(filename)s - %(funcName)s - %(lineno)d - %(message)s')
    handler.setFormatter(logging_format)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)


def get_param_value(param, data):
    """
    从请求中获取参数值
    :param param:
    :param data:
    :return:
    """
    if param in data:
        return data[param]
    else:
        return None


def dbc2sbc(ustring):
    """
    全角转半角
    全角即：Double Byte Character，简称：DBC
    半角即：Single Byte Character，简称：SBC
    :param ustring:
    :return:
    """
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x3000:
            inside_code = 0x0020
        else:
            inside_code -= 0xfee0
        if not (0x0021 <= inside_code <= 0x7e):
            rstring += uchar
            continue
        rstring += chr(inside_code)
    return rstring


def sbc2dbc(ustring):
    """
    半角转全角
    全角即：Double Byte Character，简称：DBC
    半角即：Single Byte Character，简称：SBC
    :param ustring:
    :return:
    """
    rstring = ''
    for uchar in ustring:
        inside_code = ord(uchar)
        if inside_code == 0x0020:
            inside_code = 0x3000
        else:
            if not (0x0021 <= inside_code <= 0x7e):
                rstring += uchar
                continue
        inside_code += 0xfee0
        rstring += chr(inside_code)
    return rstring
