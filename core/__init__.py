# -*- coding: utf-8 -*-

from utils import wrap_formula_exc, FormulaException

import numpy as np
import talib


class BaseSeries(object):
    '''
    https://docs.python.org/3/library/operator.html
    '''
    def __init__(self, series=np.array([])):
        self.__series = series

    @property
    def series(self):
        return self.__series

    @series.setter
    def series(self, value):
        if not isinstance(value, np.ndarray):
            raise Exception("必须是ndarray类型")
        self.__series = value

    @property
    def value(self):
        if len(self.__series) > 0:
            return self.__series[-1]
        else:
            return None

    def __getitem__(self, index):
        return self.__series[index]

    # def __setitem__(self, key, value):
    #     self.__series[key] = value
    #
    # def __delitem__(self, key):
    #     del self.__series[key]

    def __len__(self):
        """
        获取对象元素长度
        :return:
        """
        return len(self.series)

    ################## 布尔比较 ##################
    def __lt__(self, other):
        return NumericSeries(self.series < self.getOtherValue(other))

    def __gt__(self, other):
        return BoolSeries(self.series > self.getOtherValue(other))

    
    def __eq__(self, other):
        return BoolSeries(self.series == self.getOtherValue(other))

    
    def __ne__(self, other):
        return BoolSeries(self.series != self.getOtherValue(other))

    
    def __ge__(self, other):
        return BoolSeries(self.series >= self.getOtherValue(other))

    
    def __le__(self, other):
        return BoolSeries(self.series <= self.getOtherValue(other))

    
    def __sub__(self, other):
        return NumericSeries(self.series - self.getOtherValue(other))

    
    def __rsub__(self, other):
        return NumericSeries(self.getOtherValue(other) - self.series)

    
    def __add__(self, other):
        return NumericSeries(self.series + self.getOtherValue(other))

    
    def __radd__(self, other):
        return NumericSeries(self.getOtherValue(other) + self.series)

    
    def __mul__(self, other):
        return NumericSeries(self.series * self.getOtherValue(other))

    
    def __rmul__(self, other):
        return NumericSeries(self.getOtherValue(other) * self.series)

    
    def __truediv__(self, other):
        return NumericSeries(self.series / self.getOtherValue(other))

    
    def __rtruediv__(self, other):
        return NumericSeries(self.getOtherValue(other) / self.series)

    __div__ = __truediv__

    def __bool__(self):
        return len(self) > 0 and bool(self.value)

    def __and__(self, other):
        return BoolSeries(self.series & self.getOtherValue(other))

    def __or__(self, other):
        return BoolSeries(self.series | self.getOtherValue(other))

    def __invert__(self):
        return BoolSeries(~self.series)

    # fix bug in python 2
    __nonzero__ = __bool__

    def __repr__(self):
        return str(self.value)

    ####################################
    def getOtherValue(self, other):
        """
        获取真实的计算对象
        :param other:
        :return:
        """
        if isinstance(other, BaseSeries):
            return other.series
        else:
            return other




class NumericSeries(BaseSeries):
    """
    数值序列
    """
    def __init__(self, series=np.array([])):
        super(NumericSeries, self).__init__(series)




class BoolSeries(BaseSeries):
    """
    放布尔值的序列
    """
    def __init__(self, series=np.array([])):
        super(BoolSeries, self).__init__(series)





class IndicatorSeries(BaseSeries):
    """
    指标类，专门用于talib生成指标
    """
    def __init__(self, *args, **kwargs):
        args = list(args)
        if len(args) == 0:
            raise Exception('series不能为空')
        args[0] = args[0].series
        self.__series = eval(self.indicatorName)(*args, **kwargs)
        super(IndicatorSeries, self).__init__(self.__series)

    @property
    def indicatorName(self):
        raise NotImplementedError

