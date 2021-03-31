#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/9/28 10:32
# @Author  : kiway
# @Software: PyCharm



import pandas as pd
import datetime
import tushare as ts
import numpy as np
from mysqltools.mysql_connection import DbPool1, DbPool2

single_db1 = DbPool1()
single_db2 = DbPool2("strategy_data")

class DBReader:
    """
    _init_参数： configpath:配置文件路径，无须包含文件名 如../filepath/test/

    方法:
    read_tdx_1min_data 获取分钟数据
    read_ts_top_inst 获取龙虎榜机构明细
    read_ts_top_list 获取龙虎榜股票明细
    read_ts_day_data 获取日线综合数据
    read_ts_index_daily 获取指数日线数据
    read_ts_limit_list 获取每日涨停板数据
    read_ts_moneyflow_hsgt 获取沪深港通资金流数据
    read_concept_data 获取板块信息数据
    """

    def __init__(self, *args, **kwargs):
        self.dbpath = None
        self.file_used = None
        self.tradetime = {
            '1min': [
                '09:31:00', '09:32:00', '09:33:00', '09:34:00', '09:35:00', '09:36:00', '09:37:00', '09:38:00',
                '09:39:00', '09:40:00', '09:41:00', '09:42:00', '09:43:00', '09:44:00', '09:45:00', '09:46:00',
                '09:47:00', '09:48:00', '09:49:00', '09:50:00', '09:51:00', '09:52:00', '09:53:00', '09:54:00',
                '09:55:00', '09:56:00', '09:57:00', '09:58:00', '09:59:00', '10:00:00', '10:01:00', '10:02:00',
                '10:03:00', '10:04:00', '10:05:00', '10:06:00', '10:07:00', '10:08:00', '10:09:00', '10:10:00',
                '10:11:00', '10:12:00', '10:13:00', '10:14:00', '10:15:00', '10:16:00', '10:17:00', '10:18:00',
                '10:19:00', '10:20:00', '10:21:00', '10:22:00', '10:23:00', '10:24:00', '10:25:00', '10:26:00',
                '10:27:00', '10:28:00', '10:29:00', '10:30:00', '10:31:00', '10:32:00', '10:33:00', '10:34:00',
                '10:35:00', '10:36:00', '10:37:00', '10:38:00', '10:39:00', '10:40:00', '10:41:00', '10:42:00',
                '10:43:00', '10:44:00', '10:45:00', '10:46:00', '10:47:00', '10:48:00', '10:49:00', '10:50:00',
                '10:51:00', '10:52:00', '10:53:00', '10:54:00', '10:55:00', '10:56:00', '10:57:00', '10:58:00',
                '10:59:00', '11:00:00', '11:01:00', '11:02:00', '11:03:00', '11:04:00', '11:05:00', '11:06:00',
                '11:07:00', '11:08:00', '11:09:00', '11:10:00', '11:11:00', '11:12:00', '11:13:00', '11:14:00',
                '11:15:00', '11:16:00', '11:17:00', '11:18:00', '11:19:00', '11:20:00', '11:21:00', '11:22:00',
                '11:23:00', '11:24:00', '11:25:00', '11:26:00', '11:27:00', '11:28:00', '11:29:00', '11:30:00',
                '13:01:00', '13:02:00', '13:03:00', '13:04:00', '13:05:00', '13:06:00', '13:07:00', '13:08:00',
                '13:09:00', '13:10:00', '13:11:00', '13:12:00', '13:13:00', '13:14:00', '13:15:00', '13:16:00',
                '13:17:00', '13:18:00', '13:19:00', '13:20:00', '13:21:00', '13:22:00', '13:23:00', '13:24:00',
                '13:25:00', '13:26:00', '13:27:00', '13:28:00', '13:29:00', '13:30:00', '13:31:00', '13:32:00',
                '13:33:00', '13:34:00', '13:35:00', '13:36:00', '13:37:00', '13:38:00', '13:39:00', '13:40:00',
                '13:41:00', '13:42:00', '13:43:00', '13:44:00', '13:45:00', '13:46:00', '13:47:00', '13:48:00',
                '13:49:00', '13:50:00', '13:51:00', '13:52:00', '13:53:00', '13:54:00', '13:55:00', '13:56:00',
                '13:57:00', '13:58:00', '13:59:00', '14:00:00', '14:01:00', '14:02:00', '14:03:00', '14:04:00',
                '14:05:00', '14:06:00', '14:07:00', '14:08:00', '14:09:00', '14:10:00', '14:11:00', '14:12:00',
                '14:13:00', '14:14:00', '14:15:00', '14:16:00', '14:17:00', '14:18:00', '14:19:00', '14:20:00',
                '14:21:00', '14:22:00', '14:23:00', '14:24:00', '14:25:00', '14:26:00', '14:27:00', '14:28:00',
                '14:29:00', '14:30:00', '14:31:00', '14:32:00', '14:33:00', '14:34:00', '14:35:00', '14:36:00',
                '14:37:00', '14:38:00', '14:39:00', '14:40:00', '14:41:00', '14:42:00', '14:43:00', '14:44:00',
                '14:45:00', '14:46:00', '14:47:00', '14:48:00', '14:49:00', '14:50:00', '14:51:00', '14:52:00',
                '14:53:00', '14:54:00', '14:55:00', '14:56:00', '14:57:00', '14:58:00', '14:59:00', '15:00:00'],
            '5min': [
                '09:35:00', '09:40:00', '09:45:00', '09:50:00', '09:55:00', '10:00:00', '10:05:00', '10:10:00',
                '10:15:00', '10:20:00', '10:25:00', '10:30:00', '10:35:00', '10:40:00', '10:45:00', '10:50:00',
                '10:55:00', '11:00:00', '11:05:00', '11:10:00', '11:15:00', '11:20:00', '11:25:00', '11:30:00',
                '13:05:00', '13:10:00', '13:15:00', '13:20:00', '13:25:00', '13:30:00', '13:35:00', '13:40:00',
                '13:45:00', '13:50:00', '13:55:00', '14:00:00', '14:05:00', '14:10:00', '14:15:00', '14:20:00',
                '14:25:00', '14:30:00', '14:35:00', '14:40:00', '14:45:00', '14:50:00', '14:55:00', '15:00:00'],
            '15min': [
                '09:45:00', '10:00:00', '10:15:00', '10:30:00', '10:45:00', '11:00:00', '11:15:00', '11:30:00',
                '13:15:00', '13:30:00', '13:45:00', '14:00:00', '14:15:00', '14:30:00', '14:45:00', '15:00:00'],
            '30min': [
                '10:00:00', '10:30:00', '11:00:00', '11:30:00', '13:30:00', '14:00:00', '14:30:00', '15:00:00',
                '13:00:00']}
        self.allcode_index = [1, 16, 905, 906, 300, 399001, 399006, 399005, 399300]
        # ts.set_token('e6e5601134d8d0f15d2192e65e2551998dc2027c29f776834d5cd8f7')
        # ts.set_token(df_config.loc[0, 'tushare_token'])
        try:
            pro = ts.pro_api()
        except:
            print('tushare连接出错，使用配置文件中token重新尝试连接')
            try:
                # ts.set_token(df_config.loc[0, 'tushare_token'])
                pro = ts.pro_api()
            except Exception:
                raise ConnectionError('使用配置文件中token连接tushare失败，请联系管理员')
        try:
            df_opendate = pro.query('trade_cal', start_date='20150101', end_date='20991231')  # 获取交易日
            df_opendate = df_opendate[df_opendate.is_open == 1]['cal_date']
            # 目前正常交易股票代码和名称
            allcode = pro.stock_basic(exchange='', fields='ts_code,list_date').rename(columns={'ts_code': 'code'})
            allcode['code'] = allcode['code'].apply(lambda x: int(x[0:6]))
            allcode['list_date'] = allcode['list_date'].apply(lambda x: f"{x[0:4]}-{x[4:6]}-{x[6:8]}")
            self.allcode = allcode['code'].to_list()
            self.__list_date = allcode
            delcode = pro.stock_basic(exchange='', list_status='D', fields='symbol,list_date,delist_date')
            delcode['symbol'] = delcode['symbol'].apply(lambda x: x.strip('T'))
            delcode['symbol'] = delcode['symbol'].astype(int)
            delcode = delcode.rename(columns={'symbol': 'code'})
            codename = pro.stock_basic(exchange='', list_status='L', fields='symbol,name')
            codename['symbol'] = codename['symbol'].astype(int)
            codename = codename.rename(columns={'symbol': 'code'})
            # 退市股
            self.__delcode = delcode['code'].to_list()
            # 非ST股票
            df_st = pro.namechange(start_date=20140101, fields='ts_code,name,start_date,end_date,change_reason')
            df_st = df_st[df_st['name'].str.contains('\*|ST')]
            df_st['code'] = df_st['ts_code'].apply(lambda x: int(x[0:6]))
            df_st['start_date'] = df_st['start_date'].apply(lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:]))
            df_st['end_date'] = df_st['end_date'].apply(
                lambda x: '{0}-{1}-{2}'.format(x[0:4], x[4:6], x[6:]) if x is not None else '2099-09-09')
            df_st.sort_values(by='code', inplace=True)
            df_st.reset_index(inplace=True)
            df_st = df_st[['code', 'start_date', 'end_date']]
            self.__stcode = df_st
            # 交易日历——日
            self.open_date = df_opendate.apply(lambda x: x[0:4] + '-' + x[4:6] + '-' + x[6:])
        except Exception as e:
            raise Exception('_init_过程发生错误 ', e)


    def __new_clean(self, df, start, newdrop):
        if isinstance(newdrop, int):
            pass
        else:
            raise Exception(f'newdrop必须为int，输入值:{newdrop}')
        if newdrop == 0:
            return df
        start = start.replace('"', '')
        df_list_date = \
            self.__list_date[
                self.__list_date['list_date'] >= self.get_opendate(time=start, shift=newdrop)].copy(deep=True)
        df_list_date['list_date'] = \
            df_list_date['list_date'].apply(lambda x: self.get_opendate(time=x, forward=newdrop))
        df_list_date = df_list_date.groupby('code').agg('max').reset_index()
        df = pd.merge(df, df_list_date, on='code', how='left')
        df['list_date'] = df['list_date'].fillna('0')
        df = df[df['list_date'] <= df['date']]
        df.drop(['list_date'], axis=1, inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    @staticmethod
    def get_tableinfo_cols(dbfile, tablename):
        # \ df_tableinfo = pd.read_sql('PRAGMA table_info([' + tablename + '])', con=sqlite3.connect(str(dbfile)))
        con = DbPool1(dbfile).get_con()
        cur = con.cursor()
        cur.execute(rf"desc {tablename}")
        result = cur.fetchall()
        # for i in result:
        #     col.append(i[0])
        col = [i[0] for i in result]
        return col


    # 处理并检查输入的time选择区间
    @staticmethod
    def __check_mintime(start, end, dt_start, dt_end):
        if start is not None:
            assert isinstance(start, str) and len(start) == 8 and start.replace(':', '').isdigit() and start[
                                                                                                       0: 2] < '24' \
                   and start[3: 5] < '60' and start[6: 8] < '60', 'time_start必须为形如09:30:00的字符,且大小符合时间进制'
        if end is not None:
            assert isinstance(end, str) and len(end) == 8 and end.replace(':', '').isdigit() and end[0: 2] < '24' and \
                   end[3: 5] < '60' and end[6: 8] < '60', 'time_end必须为形如09:30:00的字符,且大小符合时间进制'
        if start is not None and end is not None:
            str_mintime = ' AND time >= "' + start + '" AND time <= ' + '"' + end + '"'
            dt_start = f"{dt_start[:-9]}{start}{dt_start[0]}"
            dt_end = f"{dt_end[:-9]}{end}{dt_end[0]}"
        elif start is not None and end is None:
            str_mintime = ' AND time >= "' + start + '"'
            dt_start = f"{dt_start[:-9]}{start}{dt_end[0]}"
        elif start is None and end is not None:
            str_mintime = ' AND time <= "' + end + '"'
            dt_end = f"{dt_end[:-9]}{dt_end[0]}'"
        else:
            str_mintime = ''
        return str_mintime, dt_start, dt_end

    # 处理并检查时间输入，转变为sql语句
    @staticmethod
    def check_time(time):
        """
        :param time: 需要转换为YYYY-mm-dd格式str的日期，支持格式datetime.date, datetime.datetime, str, int

        :return: YYYY-mm-dd格式str的日期.
        """

        if isinstance(time, int):
            if 19000000 < time:
                time = str(time)
                str_time = time[0:4] + '-' + time[4:6] + '-' + time[6:]
            else:
                raise ValueError('数值型start,time必须为8位数int,如20180808,当前输入:{}'.format(time))
        elif isinstance(time, str):
            if len(time) == 10:
                time = datetime.datetime.strptime(time, '%Y-%m-%d')
            elif len(time) == 8:
                time = datetime.datetime.strptime(time, '%Y%m%d')
            elif len(time) == 19:
                time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            else:
                raise ValueError('输入str类型时间仅支持"2010-08-08"或"20100808"')
            str_time = time.strftime('%Y-%m-%d')

        elif isinstance(time, (datetime.datetime, datetime.date)):
            try:
                str_time = time.strftime('%Y-%m-%d')
            except ValueError:
                raise ValueError('datetime型start,time必须符合YYYY-MM-DD hh:mm:ss,如2018-08-08 00:00:00')
        else:
            raise ValueError('时间格式错误:{}'.format(time))
        return str_time

    @staticmethod
    def __check_dbtablename(dbname, tablename):
        assert isinstance(dbname, str), 'dbname必须为str，如tushare_data.sqlite3或tushare_data'
        assert isinstance(tablename, str), 'tablename必须为str如ts_day_data'
        if '.sqlite3' in dbname:
            pass
        else:
            dbname = dbname + '.sqlite3'
        return dbname

    # 确定shift和forward时间
    def __check_timechange(self, start, end, shift, forward, minmode=False):
        if not isinstance(shift, int) or not isinstance(forward, int) or shift < 0 or forward < 0:
            raise ValueError('shift必须为大于0的int')
        else:
            if shift == 0:
                str_start = start
                pass
            else:
                str_start = self.open_date[self.open_date < start].tail(shift).tolist()[0]

            if forward == 0:
                str_end = end
                pass
            else:
                if len(self.open_date[self.open_date > end]) > 0:
                    str_end = self.open_date[self.open_date > end].head(forward).tolist()[-1]
                else:
                    raise ValueError('forward时间过长,不能穿越到未来！')
            if minmode:
                str_start = '{0}{1}{2}{0}'.format('"', str_start, ' 00:00:00')
                str_end = '{0}{1}{2}{0}'.format('"', str_end, ' 23:00:00')
            else:
                str_start = '{0}{1}{0}'.format('"', str_start)
                str_end = '{0}{1}{0}'.format('"', str_end)
            return str_start, str_end

    # 检查股票代码输入是否正确并生成sql的code查询语句
    # @staticmethod
    def __check_code(self, code, dbname_code, indexmode=False):
        if code is None:
            # str_code = ' '
            if indexmode:
                code = self.allcode_index
            else:
                code = self.allcode
        if isinstance(code, list):
            code = '(' + ','.join(map(lambda x: str(int(x)), code)) + ')'
            str_code = dbname_code + ' in ' + code + ' AND '
        elif isinstance(code, int):
            code = '(' + str(code) + ')'
            str_code = dbname_code + ' in ' + code + ' AND '
        elif isinstance(code, pd.Series):
            code = '(' + ','.join(map(lambda x: str(int(x)), code.to_list())) + ')'
            str_code = dbname_code + ' in ' + code + ' AND '
        else:
            raise ValueError('输入的code为{},请保证code格式为 list 或 int'.format(type(code)))

        return str_code

    # 检查fields是否有效并处理fields格式
    @staticmethod
    def __check_fields(fields, standard_fields):
        # 全选处理
        if fields == '*':
            return fields
        else:
            # str形式处理
            if isinstance(fields, str):
                fieldslist = fields.split(',')
                errorlist = []
                for column in fieldslist:
                    if column in standard_fields:
                        pass
                    else:
                        errorlist.append(column)
                if len(errorlist) == 0:
                    return fields
                else:
                    raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))

            # list形式处理
            if hasattr(fields, "__iter__"):
                errorlist = []
                for column in fields:
                    if column in standard_fields:
                        pass
                    else:
                        errorlist.append(column)
                if len(errorlist) == 0:
                    str_fields = ','.join(fields)
                    return str_fields
                else:
                    raise ValueError('当前查询表内不存在列名：{}'.format(errorlist))

    @staticmethod
    def __fields_append(fields, time_start=None, time_end=None, noncode=False):
        fieldsdrop = {'code': 0, 'date': 0, 'time': 0}
        if fields == '*':
            return fieldsdrop, fields
        fieldslist = fields.split(',')
        if 'date' in fieldslist:
            pass
        else:
            fieldsdrop['date'] = 1
            fields = 'date,' + fields
        if 'code' in fieldslist or noncode:
            pass
        else:
            fieldsdrop['code'] = 1
            fields = 'code,' + fields
        if time_start is not None or time_end is not None:
            if 'time' in fieldslist:
                pass
            else:
                fieldsdrop['time'] = 1
                fields = 'time,' + fields
        return fieldsdrop, fields

    @staticmethod
    def __fields_drop(df, fieldsdrop):
        dropfield = [x for x in fieldsdrop.keys() if fieldsdrop[x] == 1]
        if len(dropfield) > 0:
            df.drop(dropfield, axis=1, inplace=True)
        return df

    # 剔除ST股
    def __st_clean(self, df, dbname_code, start, fields, stdrop):
        if not stdrop:
            return df
        start = start.replace('"', '')
        if (dbname_code in fields and 'date' in fields) or fields == '*':
            df_stcode = self.__stcode[self.__stcode['end_date'] >= start]
            df_stcode = df_stcode.sort_values(by=['code', 'start_date'])
            df_stcode.reset_index(inplace=True, drop=True)
            # df_stcode.drop_duplicates(subset=['code'], keep='first', inplace=True)
            df_stcode = df_stcode.groupby('code').agg({'start_date': 'min', 'end_date': 'max'}).reset_index()
            df = pd.merge(df, df_stcode.rename(columns={
                'start_date': 'st_kaishi', 'end_date': 'st_jieshu'}), on='code', how='left')
            df['st_kaishi'] = df['st_kaishi'].fillna('2099-09-09')
            df['st_jieshu'] = df['st_jieshu'].fillna('2099-09-09')
            df = df[~((df['st_kaishi'] <= df['date']) & (df['date'] <= df['st_jieshu']))]
            df.drop(['st_kaishi', 'st_jieshu'], axis=1, inplace=True)
            df.reset_index(drop=True, inplace=True)
        else:
            raise ValueError('stdrop为True时，fields必须为*或包含股票代码，日期字段（code和date）')
        return df

    # 剔除退市股
    def __del_clean(self, df, dbname_code, fields, deldrop):
        if not deldrop:
            return df
        if dbname_code in fields or fields == '*':
            df = df[~df[dbname_code].isin(self.__delcode)]
            df = df.reset_index().drop(['index'], axis=1)
        else:
            raise ValueError('deldrop为True时，fields必须为*或包含股票代码有效字段（code或code）')
        return df

    # 剔除科创板
    @staticmethod
    def __star_clean(stardrop, dbname_code):
        if isinstance(stardrop, bool):
            if stardrop:
                str_stardrop = ' AND ' + dbname_code + '<=650000'
            else:
                str_stardrop = ''
        else:
            raise ValueError('stardrop参数为bool值')
        return str_stardrop

    def get_timesection(self, start, end, shift=0, forward=0, mode='str'):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param mode: 时间格式，默认str，支持str datetime int

        :return: yyyy-mm-dd格式str的日期组成的list.
        """

        assert isinstance(shift, int) and isinstance(forward, int), 'shift或forward的值必须为≥0的int'
        assert shift >= 0 and forward >= 0, 'shift,forward为非负整数'
        assert mode in ['str', 'datetime', 'int', 'date'], 'mode参数仅可选str，datetime，int,date'
        # time格式检查
        start = self.get_opendate(time=start, shift=shift)
        end = self.get_opendate(time=end, forward=forward)
        if start > end:
            raise ValueError('获取交易日历的开始日期不能大于截止日期')
        timesection = list(self.open_date[(self.open_date >= start) & (self.open_date <= end)])
        # 设定时间格式
        if mode == 'str':
            pass
        elif mode == 'datetime':
            timesection = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in timesection]
        elif mode == 'date':
            timesection = [datetime.datetime.strptime(x, '%Y-%m-%d').date() for x in timesection]
        elif mode == 'int':
            timesection = [int(x.replace('-', '')) for x in timesection]
        else:
            pass
        return timesection

    def get_opendate(self, time, shift=0, forward=0, mode='str'):
        """
        :param time: 基准日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param mode: 时间格式，默认str，支持str datetime int

        :return: yyyy-mm-dd格式str的交易日期.
        """

        assert isinstance(shift, int) and isinstance(forward, int), 'shift或forward的值必须为≥0的int'
        assert shift >= 0 and forward >= 0, 'shift和forward为非负整数'
        assert not (shift > 0 and forward > 0), 'shift或forward只能选一个'
        assert mode in ['str', 'datetime', 'int', 'date'], 'mode参数仅可选str，datetime，int,date'
        if not isinstance(shift, int) or not isinstance(forward, int):
            raise ValueError('shift或forward的值必须为≥0的int')
        if shift > 0 and forward > 0:
            raise ValueError('shift或forward只能选一个')
        # time格式检查
        stime = self.check_time(time=time)
        # shift 确认
        if shift > 0:
            stime = self.open_date[self.open_date < stime].tail(shift).tolist()[0]
        else:
            pass
        # forward 确认
        if forward > 0:
            stime = self.open_date[self.open_date > stime].head(forward).tolist()[-1]
        else:
            pass
        # 设定时间格式
        if mode == 'str':
            return stime
        elif mode == 'datetime':
            return datetime.datetime.strptime(stime, '%Y-%m-%d')
        elif mode == 'date':
            return datetime.datetime.strptime(stime, '%Y-%m-%d').date()
        elif mode == 'int':
            return int(stime.replace('-', ''))

    def read_ts_day_data(
            self, start, end, fields='*', code=None, shift=0, forward=0, newdrop=0,
            stdrop=True, deldrop=False, stardrop=True):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param newdrop: 新股上市多少交易日内不交易，默认0，仅支持int
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True

        :return: dataframe格式数据表.
        """

        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols("mytest", 'stockdata')
        # col = self.get_tableinfo_cols("L1_tushare_data", 'ts_day_data')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'stockdata' + ' WHERE ' + str_code + '(' \
            + dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
        try:
            connect = DbPool1("mytest").get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()

        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')

        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__new_clean(df=df, start=str_start, newdrop=newdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        else:
            pass
        return df


    def read_ts_index_daily(
            self, start, end, fields='*', code=None, shift=0, forward=0):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 09:00:00'), str('20180908')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 600012]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int

        :return: dataframe格式数据表.
        """

        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tushare_data', 'ts_index_daily')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code, indexmode=True)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'ts_index_daily' + \
            ' WHERE ' + str_code + '(' + dbname_date \
            + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
            if len(df) > 0:
                df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
            return df
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')

    def read_ts_limit_list(
            self, start, end, fields='*', code=None, shift=0, forward=0,
            stdrop=True, deldrop=False, stardrop=True, direction='U'):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2019-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True
        :param stardrop: 是否剔除科创板股，True剔除，默认True
        :param direction: 输出涨停板还是跌停板，U涨停板，D跌停板，默认U

        :return: dataframe格式数据表.
        """

        if direction in ['U', 'D']:
            str_direction = ' AND ts_limit="' + direction + '" '
        else:
            raise ValueError('type必须为U或者D')
        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tushare_data', 'ts_limit_list')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_pct_chg = ' AND pct_chg < 11 '
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'ts_limit_list' + ' WHERE ' + str_code + '(' + dbname_date \
            + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_direction + str_stardrop + str_pct_chg
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        else:
            pass
        return df


    def read_ts_top_list(
            self, start, end, fields='*', code=None, shift=0, forward=0,
            stdrop=True, deldrop=False, stardrop=True):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20200808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[16, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True

        :return: dataframe格式数据表.
        """

        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tushare_data', 'ts_top_list')

        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'ts_top_list' + ' WHERE ' + str_code + '(' + dbname_date \
            + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        else:
            pass
        return df

    def read_ts_top_inst(
            self, start, end, fields='*', code=None, shift=0, forward=0,
            combine=False, stdrop=True, deldrop=False, stardrop=True):
        """
        :param start: 开始日期，必选，支持int(20180809), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param combine: 日内同只股票龙虎榜机构明细数据是否合并为一行，True合并，默认False，参数combie为True时，fields参数必须为*或包含code,sell_rate,buy_rate
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True

        :return: dataframe格式数据表.
        """

        if not isinstance(combine, bool):
            raise ValueError('combine必须为True 或 False')
        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tushare_data.sqlite3', 'ts_top_inst')
        # if index_col == dbname_code and stdrop:
        # 	raise ValueError('选择index为股票时，不能剔除ST股')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'ts_top_inst' + ' WHERE ' + str_code + '(' + dbname_date \
            + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
        if combine and str_fields != '*':
            checkfields = str_fields.split(',')
            lackparanum = [1 for x in [dbname_code, 'sell_rate', 'buy_rate'] if x not in checkfields]
            if sum(lackparanum) >= 1:
                raise ValueError('参数combie为True时，fields参数必须为*或包含code,sell_rate,buy_rate')
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            if combine:
                dfgroup = df.groupby(['code', 'date'])
                df = dfgroup.sum().reset_index()
                df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        return df

    def read_ts_moneyflow_hsgt(
            self, start, end, fields='*', shift=0, forward=0):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param shift: 往前推的时间，默认0，仅支持int

        :param forward: 往后推的时间，默认0，仅支持int

        :return: dataframe格式数据表.
        """

        dbname_date = 'date'
        col = self.get_tableinfo_cols('L1_tushare_data', 'ts_moneyflow_hsgt')

        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields, noncode=True)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'ts_moneyflow_hsgt' + ' WHERE ' + '(' + dbname_date + '>=' \
            + str_start + ' AND ' + dbname_date + '<=' + str_end + ')'
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        return df

    def read_tdx_1min_data(
            self, start, end, fields='*', code=None, shift=0, forward=0,
            time_start=None, time_end=None):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param time_start: 开始时间，默认None，支持str如'09:35:30'
        :param time_end: 结束时间，默认None，支持str如'09:35:30'

        :return: dataframe格式数据表.
        """

        dbname_date = 'datetime'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tdx_1min_data', 'tdx_1min_data')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_start, str_end = \
            self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward, minmode=True)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)
        str_time, str_start, str_end = self.__check_mintime(
            start=time_start, end=time_end, dt_start=str_start, dt_end=str_end
        )
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'tdx_1min_data' + ' WHERE ' + str_code + ' (' + \
            dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + str_time + ')'
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        return df

    def read_concept_data(
            self, dictcode=False, dictconcept=False, dfcode=False, dfconcept=False, stardrop=True, dropstandard=None,
            aimcode=None, rawconcept=False, codemode='int'):
        """
        :param dictcode: 是否返回字典格式股票代码-所属版块，True返回，默认False（和其余参数4选1）
        :param dictconcept: 是否返回字典格式板块-包含股票，True返回，默认False（和其余参数4选1）
        :param  dfcode: 是否返回dataframe格式股票代码所属版块，True返回，默认False（和其余参数4选1）
        :param dfconcept: 是否返回字典格式板块-包含股票，True返回，默认False（和其余参数4选1）
        :param stardrop: 是否剔除科创板股，True剔除，默认True
        :param dropstandard: 剔除股票数量≥dropstandard的板块，默认None，仅支持int
        :param aimcode: 只选取特定股票的股票板块信息，支持元素为int的list Series array
        :param rawconcept: 是否返回原始一对一无嵌套板块df，默认False，为True时仅返回原始板块
        :param codemode: 返回code的格式，默认int，可选str或int，为str时股票代码格式:'000016'，为int时:16

        :return: dataframe格式板块信息
        """

        assert isinstance(dictconcept, bool), 'dictconcept必须为bool'
        assert isinstance(dictcode, bool), 'dictcode必须为bool'
        assert isinstance(dfcode, bool), 'dfcode必须为bool'
        assert isinstance(dfconcept, bool), 'dfconcept必须为bool'
        assert isinstance(rawconcept, bool), 'rawconcept必须为bool'
        assert dictcode + dfcode + dfconcept + dictconcept < 2, '可选输出参数最多选择一个'
        assert codemode in ['str', 'int'], f'codemode可选int，str，输入的为{codemode}'

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code='code')
        str_sql = 'SELECT concept_name,code' + ' FROM ' + 'dc_concept_data' + ' WHERE code > 0' + str_stardrop
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            pass
        else:
            return df
        df = df[~ df['concept_name'].str.contains('涨停|触板|ST')]  # 剔除昨日涨停板块
        # 剔除股票数量＞=踢出标准的板块
        if not dropstandard:
            pass
        else:
            if isinstance(dropstandard, int) and dropstandard > 0:
                df_concount = df['concept_name'].value_counts()
                df = df[~df['concept_name'].isin(df_concount[df_concount >= dropstandard].index.to_list())]
            else:
                raise ValueError('dropstandard必须是正整数')
        if codemode == 'str':
            df['code'] = df['code'].apply(lambda x: str(int(x)).zfill(6))
        else:
            df['code'] = df['code'].apply(lambda x: int(x))

        # 剔除特定股票外的股票板块信息
        if isinstance(aimcode, list) or isinstance(aimcode, pd.Series) or isinstance(aimcode, np.ndarray):
            try:
                aimconcept = df[df['code'].isin(aimcode)]['concept_name'].unique()
                df = df[df['concept_name'].isin(aimconcept)]
            except Exception:
                raise ValueError('aimcode必须为list,Array,Series型')

        concept = df['concept_name'].unique()
        if rawconcept:
            return df
        concept = pd.DataFrame({'concept_name': concept}).reset_index().rename(columns={'index': 'concept'})
        concept['concept'] = concept['concept'].apply(lambda x: 'con' + str(x + 1))
        df = pd.merge(df, concept, how='left', on='concept_name')
        if dictcode:
            group_code = df.groupby('code')
            dict_code = {code: group_code.get_group(code)['concept'].tolist() for code in df['code'].unique()}
            return df, dict_code
        elif dictconcept:
            group_concept = df.groupby('concept')
            dict_concept = {con: group_concept.get_group(con)['code'].tolist() for con in concept['concept']}
            return df, dict_concept
        elif dfcode:
            group_code = df.groupby('code')
            dict_code = {code: group_code.get_group(code)['concept'].tolist() for code in df['code'].unique()}
            df_code = pd.DataFrame([dict_code]).T.reset_index().rename(columns={'index': 'code', 0: 'concept'})
            return df, df_code
        elif dfconcept:
            group_concept = df.groupby('concept')
            dict_concept = {con: group_concept.get_group(con)['code'].tolist() for con in concept['concept']}
            df_concept = pd.DataFrame([dict_concept]).T.reset_index().rename(columns={'index': 'concept', 0: 'code'})
            return df, df_concept
        else:
            return df

    def read_aucvol_data(
            self, start, end, fields='*', code=None, shift=0, forward=0,
            stdrop=True, deldrop=False, stardrop=True):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True

        :return: dataframe格式数据表.
        """

        dbname_date = 'date'
        dbname_code = 'code'
        col = self.get_tableinfo_cols('L1_tushare_data', 'cal_auctionvol_data')
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_fields = self.__check_fields(fields=fields, standard_fields=col)
        fieldsdrop, str_fields = self.__fields_append(str_fields)
        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + 'cal_auctionvol_data' + ' WHERE ' + str_code + '(' + dbname_date \
            + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + str_stardrop
        try:
            connect = single_db1.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保tushare_data库存在')
        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        return df


    def read_strategy(
            self, start, end, tablename, fields='*', code=None, shift=0,
            forward=0, stdrop=True, deldrop=False, stardrop=True):
        """
        :param start: 开始日期，必选，支持int(20180808), datetime('2018-08-08 00:00:00'), str('20180808')
        :param end: 结束日期 ，必选，支持同start
        :param tablename: 策略版本
        :param fields: 要从库中取出的列名,默认取所有，支持str和list[str]，例如'code,high', ['code','high']
        :param code: 代码，默认取所有，支持int如300, list如[1, '300', 399905]列表内可以是数值或str
        :param shift: 往前推的时间，默认0，仅支持int
        :param forward: 往后推的时间，默认0，仅支持int
        :param stdrop: 是否剔除st股，True剔除，默认True
        :param deldrop: 是否剔除退市股，True剔除，默认False
        :param stardrop: 是否剔除科创板股，True剔除，默认True

        :return: dataframe格式数据表
        """

        dbname_date = 'date'
        dbname_code = 'code'
        # col = self.get_tableinfo_cols('L1_tushare_data', 'cal_auctionvol_data')
        try:
            standard_fields = self.get_tableinfo_cols("L1_tushare_data", tablename)
        except Exception as e:
            raise Exception('无法获取数据表的列名，策略库无表{}或未更新配置文件,检查tablename输入或更新配置文件'.format(tablename), e)
        start_date = self.check_time(time=start)
        end_date = self.check_time(time=end)
        str_start, str_end = self.__check_timechange(start=start_date, end=end_date, shift=shift, forward=forward)
        str_code = self.__check_code(code=code, dbname_code=dbname_code)
        str_fields = self.__check_fields(fields=fields, standard_fields=standard_fields)
        fieldsdrop, str_fields = self.__fields_append(str_fields)

        str_stardrop = self.__star_clean(stardrop=stardrop, dbname_code=dbname_code)
        str_sql = \
            'SELECT ' + str_fields + ' FROM ' + tablename + ' WHERE ' + \
            str_code + '(' + dbname_date + '>=' + str_start + ' AND ' + dbname_date + '<=' + str_end + ')' + \
            str_stardrop
        try:
            connect = single_db2.get_con()
            df = pd.read_sql(str_sql, con=connect)
            connect.close()
        except Exception:
            raise ConnectionError('数据库数据获取失败，请确保strategy_data库存在')
        if len(df) > 0:
            df = self.__st_clean(df=df, dbname_code=dbname_code, start=str_start, fields=str_fields, stdrop=stdrop)
            df = self.__del_clean(df=df, dbname_code=dbname_code, fields=str_fields, deldrop=deldrop)
            df = self.__fields_drop(df=df, fieldsdrop=fieldsdrop)
        else:
            pass
        return df


if __name__ == '__main__':
    # %% 首次执行区（生成/更新配置文件）
    # DBReader.firsttime_setconfig(
    # 	dbpath=r'D:\learn\navicat\data',
    # 	)

    pass



