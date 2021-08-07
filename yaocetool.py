# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from pandas._libs.tslibs.timestamps import Timestamp
import datetime
import time

def allnan(series):
    for e in series:
        if not np.isnan(e):
            return False
    return True


def sparse(df, begin, end, sparser):
    indexname = df.index.name

    if type(begin) == str:
        time1 = pd.Timestamp(begin)
        time2 = pd.Timestamp(end)
        subdf = df[time1: time2]
    else:
        subdf = df[begin, end + 1]

    newdf = subdf.copy(deep=True)
    newdf.reset_index(drop=False, inplace=True)
    resultdf = newdf.iloc[[i for i in range(0, len(newdf)) if i > i % sparser == 0]].copy(deep=True)
    del newdf
    resultdf.set_index([indexname], inplace=True)
    return resultdf


def read_data(path, indexname='时间'):
    df = pd.read_csv(path, sep='\t', low_memory=False, encoding='GBK')
    for col in df:
        if col == '时间':
            continue
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.set_index([indexname], inplace=True)
    if indexname == '时间':
        df.index = pd.to_datetime(df.index, format='%Y年%m月%d日%H时%M分%S秒%f', errors='coerce')
    return df


def myplot(df, collist, mylinewidth=1, myfontsize=5):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['figure.figsize'] = (16, 8)
    plt.rcParams['figure.dpi'] = 300
    style.use('ggplot')
    for j in collist:
        lab = df.columns[j]
        s = df[lab]
        plt.plot(s, label=lab + "[" + str(round(min(s), 2)) + ', ' + str(round(max(s), 2)) + ']', linewidth=mylinewidth)

    #locs, labels = plt.xticks()
    #new_xticks = [str(t).split()[1][0:8] for t in labels]
    #plt.xticks(locs, labels, rotation=45, horizontalalignment='right')
    legend = plt.legend(loc='best', shadow=False, fontsize=str(myfontsize))
    legend.get_title().set_fontsize(fontsize=myfontsize)
    plt.show()

def cor(a, b):
    a = a.values.tolist()
    b = b.values.tolist()
    for i in range(0, len(a)):
        if np.isnan(a[i]) or np.isnan(b[i]):
            del (a[i])
            del [b[i]]
    return np.corrcoef(a, b)


def cor_2_df(df1, df2):
    cor_dict = {}
    for i in range(0, len(df1.columns) - 1):
        if '开关' in df1.columns[i]:
            continue
        a = df1[df1.columns[i]]
        for j in range(0, len(df2.columns) - 1):
            if '开关' in df2.columns[j]:
                continue
            b = df2[df2.columns[j]]
            cora = np.corrcoef(a, b)
            if not np.isnan(cora[0, 1]):
                cor_dict[str(i) + "---" + str(j)] = cora[0, 1]

    for e in sorted(cor_dict.items(), key=lambda kv: (kv[1], kv[0])):
        print(e)
