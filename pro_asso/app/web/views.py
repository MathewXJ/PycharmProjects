import json
import time
from flask import Flask
from flask import request, Response
from app.associate import get_asso_rlt, get_asso_rlt_json

webapp = Flask(__name__)
logger = webapp.logger


@webapp.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello'


@webapp.route("/health")
def health():
    result = {'status': 'UP'}
    return Response(json.dumps(result), mimetype='application/json')


@webapp.route('/togth', methods=['GET'])
def togth_handler():
    try:
        start = time.time()
        cont = request.args.get('cont')
        logger.debug('input content is %s', cont, exc_info=True)
        if cont:
            res_dic = get_asso_rlt(cont)
            logger.info("result : {},  costs : {} ms".format(res_dic, (time.time() - start) * 1000))
            #return Response(json.dumps(res_dic, ensure_ascii=False), mimetype='application/json')
            return json.dumps(res_dic, ensure_ascii=False)
        else:
            #return Response(json.dumps({}, ensure_ascii=False), mimetype='application/json')
            return json.dumps({}, ensure_ascii=False)
    except Exception as e:
        logger.error(str(e))


@webapp.route('/togth', methods=['POST'])
def togth_handler_new():
    try:
        start = time.time()
        # 获取输入数据对象
        req_data = request.get_data(as_text=True)
        req_data = json.loads(req_data, encoding='utf-8')
        logger.debug('input content is %s', str(req_data), exc_info=True)
        if req_data:
            res_dic = get_asso_rlt_json(req_data)
            logger.info("result : {},  costs : {} ms".format(res_dic, (time.time() - start) * 1000))
            return json.dumps(res_dic, ensure_ascii=False)
        else:
            return json.dumps({}, ensure_ascii=False)
    except Exception as e:
        logger.error(str(e))