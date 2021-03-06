# -*- coding: utf8 -*-
import datetime
import logging
import sys
import pytz
import os
import psycopg2

print('Start Delete function')

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger()
logger.setLevel(level=logging.INFO)


Host = 'postgres-3m3kw1vl.sql.tencentcdb.com'
Port = 50140
User = 'tencentdb_3m3kw1vl'
Password = '2eOwX[53Y}0d!xt'
DB = 'tencentdb_3m3kw1vl'

# Changing the time zone to Beijing. 更改时区为北京时区
tz = pytz.timezone('Asia/Shanghai')

# Looking up and deleting the 'connectionID' in the database. 查询数据库中的connectionID并删除
def delete_connection_id(connection_id):
    conn = psycopg2.connect(database=DB, user=User, password=Password, host=Host, port=Port)
    print "Opened database successfully"

    sql = 'delete from info_connectionid_shop_map where connection_id = \"%s\"'%(connection_id)
    print sql
    cur = conn.cursor()
    cur.execute(sql)
    print "Table delete successfully"

    conn.commit()
    conn.close()

def main_handler(event, context):
    print("event is %s" % event)
    if 'websocket' not in event.keys():
        return {"errNo":102, "errMsg":"not found web socket"}
    else:
        print("Start DB Request {%s}" % datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))
        delete_connection_id(event['websocket']['secConnectionID'])
        print("Finish DB Request {%s}" %datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S"))
    return event

