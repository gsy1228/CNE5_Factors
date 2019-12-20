#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
@author:
@file: clean_data.py
@time: 19-12-20 下午12:16
"""
import pandas as pd
import numpy as np
import tushare as ts
ts.set_token('90642b1dd5add88c6e35b20c912d706d7207ffad0439bbc7d2fb8990')
pro = ts.pro_bar()

# 获取市场组合数据
df_market = ts.pro_bar(ts_code='000001.SH', asset='I', start_date='20100104', end_date='20181228')

# dl = []
# year_list = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']
# for y in year_list:
#     dl.append(pd.read_csv('data/quote/daily_quote_'+y+'.csv'))

df_quote = pd.read_csv('data/quote/daily_quote_2010.csv')
temp_df = df_quote[['SecuCode', 'TradingDay', 'ClosePrice', 'PrevClosePrice', 'ret', 'Ashares']]
temp_df['LnMarketCap'] = np.log(temp_df['ClosePrice'] * temp_df['Ashares'])

# 查看缺失值
missing = temp_df.isnull().sum()
print(missing)
missing = missing[missing > 0]
missing.sort_values(inplace=True)

print('ok')

