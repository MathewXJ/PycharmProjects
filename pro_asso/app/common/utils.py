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
