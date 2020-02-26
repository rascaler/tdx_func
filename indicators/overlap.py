#Overlap Studies 重叠研究
from core import IndicatorSeries


class MovingAverageSeries(IndicatorSeries):
    @property
    def indicatorName(self):
        return 'talib.MA'


class WeightedMovingAverageSeries(IndicatorSeries):
    @property
    def indicatorName(self):
        return 'talib.WMA'


class ExponentialMovingAverageSeries(IndicatorSeries):
    @property
    def indicatorName(self):
        return 'talib.EMA'


