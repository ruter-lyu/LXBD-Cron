# -*- coding: utf-8 -*-
import os
import xmlrpclib


url = os.getenv('ODOO_URL', '')
username = os.getenv('LOGIN', '')
password = os.getenv('PASSWORD', '')
dbname = os.getenv('DB_NAME', '')
code = os.getenv('TEMP_CODE', '')

# Login using the Common web services, get the uid in return
common = xmlrpclib.ServerProxy(url + '/xmlrpc/common')
try:
    uid = common.login(dbname, username, password)
except Exception as e:
    print 'INVALID Credential:', e.message


def get_rpc_ins():
    # Logged In
    rpc = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
    return rpc


def get_ids():
    rpc = get_rpc_ins()
    params = [[['template_id.code', '=', code]], ['id', 'template_id']]
    res = rpc.execute_kw(dbname, uid, password, 'kingdee.api.cron', 'search_read', params)
    return res


def api_push():
    rpc = get_rpc_ins()
    cron_ids = get_ids()
    for cron in cron_ids:
        params = [[cron['id']]]
        try:
            rpc.execute_kw(dbname, uid, password, 'kingdee.api.cron', 'execute_api_push', params)
            result = u'>>> API Push: {} done.'.format(cron['template_id'][1])
            print result.encode('utf-8')
        except Exception as e:
            print e.message


if __name__ == "__main__":
    print "========== API Push Start =========="
    api_push()
    print "========== API Push Finished =========="
