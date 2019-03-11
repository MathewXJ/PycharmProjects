#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import tornado.httpserver
import tornado.web
import tornado.ioloop
import tornado.options
from tornado.options import define, options
import json
from app.associate import get_asso_rlt
import time

# tornado.options.define定义变量-端口号-命令行可用
define("port", default=9701, help="run port", type=int)

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates")
STATIC_PATH = os.path.join(os.path.dirname(__file__), "static")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/togth", TogthHandler),
        ]
        settings = dict(
            template_path=TEMPLATE_PATH,
            static_path=STATIC_PATH,
            debug=False
        )
        tornado.web.Application.__init__(self, handlers, **settings)


# 定义处理类型
class TogthHandler(tornado.web.RequestHandler):
    def get(self):
        # 获取url中cont参数的值
        start = time.time()
        cont = self.get_argument("cont").strip()
        if len(cont) > 0:
            res_dic = get_asso_rlt(cont)
            print("tornado result : %s,  costs : %s ms" % (res_dic, (time.time() - start) * 1000))
            self.write(json.dumps(res_dic, ensure_ascii=False))
        else:
            self.write(json.dumps({}, ensure_ascii=False))


def main():
    # 命令行参数转换 python xx.py --port=8888
    tornado.options.parse_command_line()
    # httpserver监听端口
    app = tornado.httpserver.HTTPServer(Application())
    app.listen(options.port)
    # 启动IOLoop轮循监听
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
