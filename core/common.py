# -*- coding: utf-8 -*-
from core import BaseSeries, NumericSeries, BoolSeries
import numpy as np


def getRealValue(obj):
    """
    获取真实的计算对象
    :param other:
    :return:
    """
    if isinstance(obj, BaseSeries):
        return obj.series
    else:
        return obj

def parse_series(*params, length):
    """
    对齐参数，并转换为BaseSeries
    :param param:
    :param length:
    :return:
    """
    result = []
    for i in range(len(params)):
        param = params[i]
        if isinstance(param, BaseSeries):
            result.append(param)
            continue
        if isinstance(param, float) or isinstance(param, int):
            result.append(NumericSeries(np.full(length, param)))
            continue
        if isinstance(param, bool):
            result.append(BoolSeries(np.full(length, param)))
            continue
    return result

def get_max_length(*params):
    """
    获取参数数组最大长度
    :param params:
    :return:
    """
    result = []
    for i in range(len(params)):
        param = params[i]
        if isinstance(param, BaseSeries):
            result.append(len(param.series))
            continue
        result.append(1)
    return max(result)

def validate_params(*params):
    """
    参数类型只能是bool,int,float BaseSeries，datetime
    :param params:
    :return:
    """
    for i in range(len(params)):
        param = params[i]
        t = type(param)
        if isinstance(t, int) or \
           isinstance(t, float) or \
           isinstance(t, bool) or \
           isinstance(t, BaseSeries):
            continue
        else:
            raise Exception('参数类型只能是int,float,bool,BaseSeries')

