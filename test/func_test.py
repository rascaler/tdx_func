# from tdx_func.barfeed.mysqlfeed import MysqlFeed
# from tdx_func.funcs import *
# from tdx_func.funcs import IF, LLV, HHV, COUNT, EVERY, CROSS, ZIG
# from tdx_func.indicators import MA
# import numpy as np
#
# feed = MysqlFeed('D')
# feed.addBarsFromCode(1, '2018-09-01', '2019-08-15')
#
# # data = MA(CLOSE, 10)
# # data = IF(CLOSE > OPEN, 1, 2)
# data = LLV(CLOSE, 5)
# print(LLV(CLOSE, 5))
# print(HHV(CLOSE, 5))
# print(COUNT(CLOSE > OPEN, 5))
# print(EVERY(CLOSE > OPEN, 5))
# print(CROSS(MA(CLOSE, 5), MA(CLOSE, 10)))
# # print(CLOSE.series)
# # print(data.series)
# # print(data.series)
# # data = np.where(np.array([True, False, True]), np.array([1,2,3]), np.array([4,5,6]))
#
# data = ZIG(CLOSE, 10)
# # BUY1 = ZIG(CLOSE, 10)
# # SELL1 = MA(BUY1, 2)
# # data = CROSS(BUY1, SELL1)
#
#
# pass
#
