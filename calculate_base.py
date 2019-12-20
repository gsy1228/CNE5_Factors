#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
"""
@author:
@file: clean_data.py
@time: 19-12-20 下午12:16
"""
import pandas as pd
import numpy as np


class CalculateBase(object):
    def __init__(self):
        pass

    @staticmethod
    def cal_stock_beta(ret_series):
        """
        计算单只股票的beta值
        :param ret_series:
        :return:
        """
        ret_series['beta'] = np.nan
        for i in range(len(ret_series)-252):
            temp_df = ret_series.loc[i:i+252]
            ret_series.loc[i+252, 'beta'] = temp_df['excess_ret'].cov(temp_df['excess_mret'])/np.std(temp_df['excess_mret'])
        return ret_series


if __name__ == '__main__':
    demo = CalculateBase()

    df = pd.DataFrame(columns=['TradingDay', 'ret', 'mret', 'rf'])
    df['TradingDay'] = [x.strftime('%Y-%m-%d') for x in list(pd.date_range(start='2018-01-01', end='2018-12-31'))]
    df['ret'] = df['ret'].apply(lambda x: np.random.uniform(-0.02, 0.02))
    df['mret'] = df['mret'].apply(lambda x: np.random.uniform(-0.01, 0.01))
    df['rf'] = 0.005
    df['excess_ret'] = df['ret'] - df['rf']
    df['excess_mret'] = df['mret'] - df['rf']

    demo.cal_stock_beta(df)
