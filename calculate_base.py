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

    def cal_stock_factor(self, ret_series):
        """
        计算单只股票的因子暴露度
        :param ret_series:
        :return:
        """
        ret_series['beta'] = np.nan
        ret_series['dastd'] = np.nan
        ret_series['hsigma'] = np.nan
        ret_series['ret_add'] = ret_series['ret'] + 1
        ret_series['rf_add'] = ret_series['rf'] + 1
        ret_series['cmra'] = np.nan
        for i in range(len(ret_series)-251):
            temp_df = ret_series.loc[i:i+251]
            ret_series.loc[i+251, 'beta'] = self.cal_beta(temp_df, 63)
            ret_series.loc[i+251, 'dastd'] = self.cal_dastd(temp_df, 42)
            temp_df = ret_series.loc[i:i + 251]
            ret_series.loc[i+251, 'hsigma'] = self.cal_hsigma(temp_df, 63)
            # ret_series.loc[i+251, 'cmra'] = self.cal_cmra(temp_df)
        return ret_series

    def cal_beta(self, temp_df, half_life):
        exp_weight = self.cal_exp_weight(half_life=half_life, length=252)
        beta = (temp_df['excess_ret'] * exp_weight).cov(temp_df['excess_mret'] * exp_weight) / np.std(temp_df['excess_mret'])
        return beta

    def cal_dastd(self, temp_df, half_life):
        # 需要标准化
        exp_weight = self.cal_exp_weight(half_life=half_life, length=252)
        dastd = np.std(temp_df['excess_ret']*exp_weight)
        return dastd

    @staticmethod
    def cal_cmra(temp_df):
        split_points = np.arange(0, 273, 21)
        z = []
        for period in range(1, len(split_points)):
            ret_add = temp_df.iloc[split_points[0]:split_points[period]]['ret_add']
            rf_add = temp_df.iloc[split_points[0]:split_points[period]]['rf_add']
            z.append(np.log(ret_add.values.cumprod()[-1]) - np.log(rf_add.values.cumprod()[-1]))
        cmra= np.log(1+max(z)) - np.log(1+min(z))
        return cmra

    def cal_hsigma(self, temp_df, half_life):
        # 需要标准化
        exp_weight = self.cal_exp_weight(half_life=half_life, length=252)
        hsigma = (temp_df['excess_ret']*exp_weight).mean() - temp_df['beta'].values[-1] * (temp_df['excess_mret']*exp_weight).mean()
        return hsigma

    @staticmethod
    def cal_exp_weight(half_life, length):
        """
        生成指数权重
        :param half_life:
        :param length:
        :return:
        """
        return np.cumprod(np.repeat(1/np.exp(np.log(2)/half_life), length))[::-1]


if __name__ == '__main__':
    demo = CalculateBase()

    df = pd.DataFrame(columns=['TradingDay', 'ret', 'mret', 'rf'])
    df['TradingDay'] = [x.strftime('%Y-%m-%d') for x in list(pd.date_range(start='2018-01-01', end='2018-12-31'))]
    df['ret'] = df['ret'].apply(lambda x: np.random.uniform(-0.02, 0.02))
    df['mret'] = df['mret'].apply(lambda x: np.random.uniform(-0.01, 0.01))
    df['rf'] = pow(1.02, 1/365)-1
    df['excess_ret'] = df['ret'] - df['rf']
    df['excess_mret'] = df['mret'] - df['rf']

    demo.cal_stock_factor(df)
