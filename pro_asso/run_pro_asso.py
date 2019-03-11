#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app.common.utils import init_log_settings
from app.common.config import PRO_ASSO_PORT
from app.web.views import webapp
from gevent.pywsgi import WSGIServer

init_log_settings(logger=webapp.logger)

if __name__ == '__main__':
    WSGIServer(('0.0.0.0', PRO_ASSO_PORT), webapp).serve_forever()
