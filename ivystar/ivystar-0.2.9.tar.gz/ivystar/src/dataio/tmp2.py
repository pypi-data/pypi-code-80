# -*- coding: utf-8 -*-
from pyhive import hive

conn = hive.Connection(host='192.168.50.11', port=10000, username='', database='iptv')
cursor = conn.cursor()
cursor.execute('show tables')
#cursor.execute('select * from demo_table limit 10')
#for result in cursor.fetchall():
#    print result
