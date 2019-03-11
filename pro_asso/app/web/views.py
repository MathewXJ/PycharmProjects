import json
import time
from flask import Flask
from flask import request, Response
from app.associate import get_asso_rlt

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
            return Response(json.dumps(res_dic, ensure_ascii=False), mimetype='application/json')
        else:
            return Response(json.dumps({}, ensure_ascii=False), mimetype='application/json')
    except Exception as e:
        logger.error(str(e))
