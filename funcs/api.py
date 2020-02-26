# !/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from core import NumericSeries, BoolSeries
from core.common import getRealValue, parse_series
from utils import FormulaException

def cross(s1, s2):
    """
    s1金叉s2
    :param s1:
    :param s2:
    :returns: bool序列
    :rtype: BoolSeries
    """
    series1, series2 = s1.series, s2.series
    #今日>=
    cond1 = series1 >= series2
    #昨日<
    cond2 = series1 < series2
    #右移
    cond2 = np.insert(cond2, 0, True)
    cond2 = np.delete(cond2, len(cond2) - 1)
    return BoolSeries(cond1 & cond2)

def ref(s1, n):
    series = s1.series
    if isinstance(n, int):
        n = np.full(len(s1), n)
    else:
        n = n.series
    init = np.nan if series.dtype == np.float64 else 0
    result = np.full(len(series), init, dtype=series.dtype)
    for i in range(len(series)):
        if i < n[i]:
            continue
        result[i] = series[i - n[i]]
    return NumericSeries(result)


def minimum(s1, s2):
    # s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    # if len(s1) == 0 or len(s2) == 0:
    #     raise FormulaException("minimum size == 0")
    # series1, series2 = fit_series(s1.series, s2.series)
    # s = np.minimum(series1, series2)
    return NumericSeries(np.minimum(s1.series, s2.series))


def maximum(s1, s2):
    # s1, s2 = ensure_timeseries(s1), ensure_timeseries(s2)
    # if len(s1) == 0 or len(s2) == 0:
    #     raise FormulaException("maximum size == 0")
    # series1, series2 = fit_series(s1.series, s2.series)
    # s = np.maximum(series1, series2)
    return NumericSeries(np.maximum(s1.series, s2.series))


def count(cond, n):
    """
    COUNT(X,N),统计N周期中满足X条件的周期数,若N<0则从第一个有效值开始.
    :param cond:
    :param n:
    :return:
    """
    series = cond.series
    # 先补齐 n - 1个值
    prefix = np.full(n - 1, False)
    cal = np.hstack((prefix, series))
    result = np.full(len(series), 0)
    for i in range(len(cal) - n + 1):
        result[i] = len(np.where(cal[i:i + n] == True)[0])
    return NumericSeries(result)


def every(cond, n):
    return count(cond, n) == n


def hhv(s, n):
    """
    S在N周期内的最低价
    llv（l,3）取的是前天、昨天和今天的最高价数据
    :param s:
    :param n:
    :return:
    """
    series = s.series
    # 先补齐 n - 1个值
    prefix = np.full(n - 1, series[0])
    cal = np.hstack((prefix, series))
    result = np.full(len(series), np.nan)
    for i in range(len(cal) - n + 1):
        result[i] = np.max(cal[i:i + n])
    return NumericSeries(result)


def llv(s, n):
    """
    s在n个周期内的最小值
    :param s:
    :param n:
    :return:
    """
    series = s.series
    #先补齐 n - 1个值
    prefix = np.full(n - 1, series[0])
    cal = np.hstack((prefix, series))
    result = np.full(len(series), np.nan)
    for i in range(len(cal) - n + 1):
        result[i] = np.min(cal[i:i + n])
    return NumericSeries(result)

def iif(condition, true_statement, false_statement):
    """
    :param condition: 布尔表达式
    :param true_statement:
    :param false_statement:
    :return:
    """
    s1 = getRealValue(true_statement)
    s2 = getRealValue(false_statement)
    series = np.where(condition.series, s1, s2)
    return NumericSeries(series)


ZIG_STATE_START = 0
ZIG_STATE_RISE = 1
ZIG_STATE_FALL = 2
def zig(X, N):
    """
    未来函数
    :param X:
    :param N:
    :return:
    """
    x = N / 100
    k = X.series
    #候选值，索引
    candidateVal,candidateIndex = None,None
    #波峰波谷索引集合
    peers = [0]
    z = np.zeros(len(k))
    state = ZIG_STATE_START
    for scan_i in range(1, len(k)):
        if scan_i == len(k) - 1:
            # 扫描到尾部，如果所有元素都扫描完成仍然无法判断趋势，直接连线，斜率 >0为上升， < 0为下降
            if candidateVal is None:
                peers.append(scan_i)
            else:
                if state == ZIG_STATE_RISE:
                    if k[scan_i] >= candidateVal:
                        peers.append(scan_i)
                    else:
                        peers.append(candidateIndex)
                        peers.append(scan_i)
                elif state == ZIG_STATE_FALL:
                    if k[scan_i] <= candidateVal:
                        peers.append(scan_i)
                    else:
                        peers.append(candidateIndex)
                        peers.append(scan_i)
            break

        if state == ZIG_STATE_START:
            #上升趋势第一个候选值（峰）
            if k[scan_i] >= k[0] * (1 + x):
                candidateVal,candidateIndex = k[scan_i],scan_i
                state = ZIG_STATE_RISE
            # 下降趋势第一个候选值（谷）
            elif k[scan_i] < k[0] * (1 - x):
                candidateVal, candidateIndex = k[scan_i], scan_i
                state = ZIG_STATE_FALL
        elif state == ZIG_STATE_RISE:
            #上升阶段， 如果扫描点大于候选值（峰，新的高点），就设置当前扫描点为候选值（峰，新的高点）
            if k[scan_i] >= candidateVal:
                candidateVal, candidateIndex = k[scan_i], scan_i
            # 上升阶段， 如果扫描点小于于候选值（峰）* (1-x)，候选值成为真正的峰，当前扫描点成为下降拐点
            elif k[scan_i] <= candidateVal * (1 - x):
                peers.append(candidateIndex)
                state = ZIG_STATE_FALL
                candidateVal, candidateIndex = k[scan_i], scan_i
        elif state == ZIG_STATE_FALL:
            # 下降阶段， 如果扫描点小于候选值（谷，新的低点），就设置当前扫描点为候选值（谷，新的低点）
            if k[scan_i] <= candidateVal:
                candidateVal, candidateIndex = k[scan_i], scan_i
            # 下降阶段， 如果扫描点大于候选值（谷，新的低点）* (1+x)，候选值成为真正的谷，当前扫描点成为上升拐点
            elif k[scan_i] >= candidateVal * (1 + x):
                peers.append(candidateIndex)
                state = ZIG_STATE_RISE
                candidateVal, candidateIndex = k[scan_i], scan_i
    print(peers)
    for i in range(len(peers) - 1):
        peer_start_i = peers[i]
        peer_end_i = peers[i + 1]
        start_value = k[peer_start_i]
        end_value = k[peer_end_i]
        a = (end_value - start_value) / (peer_end_i - peer_start_i)  # 斜率
        for j in range(peer_end_i - peer_start_i + 1):
            z[j + peer_start_i] = start_value + a * j
    return NumericSeries(z)


def barslast(cond):
    """
    距离上一个周期为True的天数
    :param cond:
    :return:
    """
    cond = cond.series
    length = len(cond)
    #获取符合条件的索引
    result = []
    indexs = np.where(cond == True)
    indexs = indexs[0]
    indexLength = len(indexs)
    if len(indexs) == 0:
        return NumericSeries(np.full(length, 0))
    for i in range(indexLength):
        if i == 0:
            result += [0] * indexs[0]
        if i == indexLength - 1:
            result += list(range(length - indexs[i]))
            continue
        result += list(range(indexs[i + 1] - indexs[i]))
    return NumericSeries(np.array(result))


def tdx_rang(A, B, C):
    A, B, C = parse_series(A, B, C)
    Aseries, Bseries, Cseries = A.series, B.series, C.series
    result = []
    for i in range(len(A.series)):
        if Aseries[i] > Bseries[i] and Aseries[i] < Cseries[i]:
            result.append(True)
        else:
            result.append(False)
    return result

