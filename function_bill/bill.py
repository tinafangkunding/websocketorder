# -*- coding: utf-8 -*-

import sys
import logging
import psycopg2
import json
import os
import requests

print('Loading function')

logger = logging.getLogger()
apiid = os.getenv('apiid')
sendbackHost = "http://set-websocket.cb-common.apigateway.tencentyun.com/" + apiid


def send(connectionID, data):
    retmsg = {}
    retmsg['websocket'] = {}
    retmsg['websocket']['action'] = "data send"
    retmsg['websocket']['secConnectionID'] = connectionID
    retmsg['websocket']['dataType'] = 'text'
    retmsg['websocket']['data'] = data
    print("send %s to %s" % (json.dumps(data).decode('unicode-escape'), connectionID))
    requests.post(sendbackHost, json=retmsg)


def main_handler(event, context):
    logger.info("start main handler")

    res = {"error_code": 0, "error_msg": "success"}


    text = json.loads(event["body"])
    user = text["user"]
    addr = text["addr"]
    telephone = text["telephone"]

    shop_name = text["shop_name"]
    dish = text["dish"]

    if telephone is None or user is None or shop_name is None:
        res['error_code'] = -1
        res['error_msg'] = 'telephone or username or shop name is empty'
        return res

    host = 'postgres-3m3kw1vl.sql.tencentcdb.com'
    port = 50140
    user = 'tencentdb_3m3kw1vl'
    password = '2eOwX[53Y}0d!xt'
    dbname = 'tencentdb_3m3kw1vl'

    conn = psycopg2.connect(database=dbname, user=user, password=password, host=host, port=port)

    cur = conn.cursor()

    # 查询一下用户购买的套餐店铺是否存在
    sql_get_connection_id = "SELECT shop_name, connection_id from info_connectionid_shop_map where shop_name =\'%s\'" % (shop_name)
    cur.execute(sql_get_connection_id)

    rows = cur.fetchall()
    if len(rows) == 0:
        res['error_code'] = -2
        res['error_msg'] = 'the shop is not working now, please wait...'
        return res

    for row in rows:
        shop_name = row[0]
        connection_id = row[1]
        msg = "shop : %s , you get a bill  %s, addr %s , telephone %s " % (shop_name, dish, addr, telephone)
        send(connection_id, msg)

    res = {"error_code": 0, "error_msg": "success"}

    conn.commit()
    conn.close()

    return res