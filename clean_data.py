#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
@author:
@file: clean_data.py
@time: 19-12-20 下午12:16
"""
import time
import pandas as pd
import numpy as np
import tushare as ts
from calculate_base import CalculateBase
# ts.set_token('90642b1dd5add88c6e35b20c912d706d7207ffad0439bbc7d2fb8990')

# pro = ts.pro_api()
cal = CalculateBase()

# 获取市场组合数据(A股指数)
# df_market = pro.index_daily(ts_code='000002.SH', start_date='20100104', end_date='20181228')
# df_market['pct_chg'] = df_market['pct_chg']/100
# df_market.to_csv('data/df_market.csv', index=0)

# 获取无风险利率数据(Shibor利率,'on'为隔夜)
# df_free_risk_1 = pro.shibor(start_date='20100104', end_date='20181228')
# df_free_risk_2 = pro.shibor(start_date='20100104', end_date='20101227')
# df_free_risk = pd.concat([df_free_risk_1, df_free_risk_2])
# df_free_risk.to_csv('data/df_free_risk.csv', index=0)

# 批量读取数据
# dl = []
# # year_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
# year_list = ['2010', '2011']
# for y in year_list:
#     dl.append(pd.read_csv('data/quote/daily_quote_'+y+'.csv'))
# df_quote = pd.concat(dl)[['SecuCode', 'TradingDay', 'ClosePrice', 'PrevClosePrice', 'ret', 'Ashares']]
# df_quote.to_csv('data/df_quote_demo.csv', index=0)

df_market = pd.read_csv('data/df_market.csv')[['trade_date', 'pct_chg']]
df_free_risk = pd.read_csv('data/df_free_risk.csv')[['date', 'on']]
df_quote = pd.read_csv('data/df_quote_demo.csv')

df_market['trade_date'] = df_market['trade_date'].apply(lambda x: "-".join([str(x)[0:4], str(x)[4:6], str(x)[6:8]]))
df_free_risk['date'] = df_free_risk['date'].apply(lambda x: "-".join([str(x)[0:4], str(x)[4:6], str(x)[6:8]]))
df_market = df_market.rename(columns={'trade_date': 'TradingDay', 'pct_chg': 'mret'})
df_free_risk = df_free_risk.rename(columns={'date': 'TradingDay', 'on': 'rf'})
df_mret_rf = pd.merge(df_market, df_free_risk, on='TradingDay')

df_quote['LnMarketCap'] = np.log(df_quote['ClosePrice'] * df_quote['Ashares'])
df_quote = pd.merge(df_quote, df_mret_rf, on='TradingDay')
df_quote['rf'] = df_quote['rf'].apply(lambda x: pow((x/100+1), 1./365)-1)
df_quote['excess_ret'] = df_quote['ret'] - df_quote['rf']
df_quote['excess_mret'] = df_quote['mret'] - df_quote['rf']

# 删除缺失收益率的数据
df_quote = df_quote.drop(df_quote[df_quote['ret'].isnull()].index)

# 查看缺失值
missing = df_quote.isnull().sum()
print(missing)
missing = missing[missing > 0]
missing.sort_values(inplace=True)

# 因子暴露度计算
time1 = time.time()
shares_data = []
count = 0
groups = df_quote.groupby('SecuCode')
for share_data in groups:
    ret_series = share_data[1]
    ret_copy = ret_series.copy()
    ret_copy.sort_values('TradingDay', inplace=True)
    ret_copy = ret_copy.reset_index(drop=True)
    res = cal.cal_stock_factor(ret_copy)
    shares_data.append(res)
    count += 1
    print('完成第%s只股票计算' % count)
time2 = time.time()
print('因子计算：%s' % (time2-time1))
data = pd.concat(shares_data)
time3 = time.time()
print('数据合并：%s' % (time3-time2))
print('finished')


