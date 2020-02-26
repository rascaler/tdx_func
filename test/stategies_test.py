# !/usr/bin/env python
# -*- coding: utf-8 -*-
from tdx_func.barfeed.mysqlfeed import MysqlFeed
from tdx_func.funcs import *
import numpy as np

# RSV:=(CLOSE-LLV(LOW,6))/(HHV(HIGH,6)-LLV(LOW,6))*100;
# K:=SMA(RSV,3,1);
# D:=SMA(K,3,1);
# J:=3*K-2*D;
# VARV:=(2*CLOSE+HIGH+LOW)/4;
# VARU:=LLV(LOW,30);
# VARA1:=HHV(HIGH,30);
# B:=EMA((VARV-VARU)/(VARA1-VARU)*100,8);
# B1:=EMA(B,5);
# LC:=REF(CLOSE,1);
# RSI:=SMA(MAX(CLOSE-LC,0),6,1)/SMA(ABS(CLOSE-LC),6,1)*100;
# 低吸:IF(CROSS(RSI,11),70,0),POINTDOT,COLORWHITE;
# VAR1:=B-B1>0 AND REF(B-B1,1)<0 AND COUNT(B-B1 <0,8) == 7;
# XG:VAR1;
from tdx_func.funcs import LLV, HHV, REF, COUNT, BARSLAST
from tdx_func.indicators import EMA

# VARV:=(2*CLOSE+HIGH+LOW)/4;
# VARU:=LLV(LOW,30);
# VARA1:=HHV(HIGH,30);
# B:=EMA((VARV-VARU)/(VARA1-VARU)*100,8);
# B1:=EMA(B,5);
# VAR2:=B-B1;
#
# TDXSTEP107:STICKLINE(B>0 AND B-B1>=0,79,80,2,0),COLORRED;
# TDXSTEP108:STICKLINE(B>0 AND B-B1<0,79,80,2,0),COLORGREEN;
# TDXSTEP109:STICKLINE(B>0 AND B-B1>=0,49,50,2,0),COLORRED;
# TDXSTEP110:STICKLINE(B>0 AND B-B1<0,49,50,2,0),COLORFF8899;
# TDXSTEP111:STICKLINE(B>0 AND B-B1>=0,19,20,2,0),COLORRED;
# TDXSTEP112:STICKLINE(B>0 AND B-B1<0,19,20,2,0),COLORGREEN;
#
# {绿红，绿柱必须>=4才能认定有效}
# VAR3:= REF(VAR2,1)<0 AND VAR2>0 AND COUNT(VAR2 < 0, 7) == 6;
# {红绿转折点，红柱必须 >= 4才能认定转折有效}
# VAR4:=REF(B-B1,1)>0 AND B-B1<0 AND COUNT(VAR2 > 0, 7) == 6;
# DRAWICON(VAR3 AND REF(B,BARSLAST(VAR4)) - B > 30,120,1);
# DRAWICON(VAR3 AND B-REF(B,REF(BARSLAST(VAR3),1) + 1) > 20 AND COUNT(VAR2<0,10)<9,120,1);

feed = MysqlFeed('D')
feed.addBarsFromCode(1, '2018-01-01', '2019-08-15')


VARV = (2 * CLOSE + HIGH + LOW) / 4
VARU = LLV(LOW, 30)
VARA1 = HHV(HIGH,30)
B = EMA((VARV-VARU)/(VARA1-VARU)*100, 8)
B1 = EMA(B, 5)
VAR2 = B - B1

# #红->绿
# GREEN = (B-B1 < 0) & (REF(B-B1, 1) > 0)
# GREELAST = BARSLAST(GREEN)
# #绿->红
# RED = (B-B1 > 0) & (REF(B-B1, 1) < 0)
# REDLAST = BARSLAST(RED)


VAR3 = (REF(VAR2, 1) < 0) & (VAR2 > 0) & (COUNT(VAR2 < 0, 7) == 6)
VAR4 = (REF(VAR2, 1) > 0) & (VAR2 < 0) & (COUNT(VAR2 > 0, 7) == 6)

BUY = VAR3 & (REF(B, BARSLAST(VAR4)) - B > 30)
BUY2 = VAR3 & (B-REF(B, REF(BARSLAST(VAR3), 1) + 1) > 20) & (COUNT(VAR2 < 0, 10) < 9)

# buyIndex = np.where(BUY == True)
#
# buyIndex2 = np.where(BUY2 == True)

for i in range(len(BUY.series)):
    if BUY.series[i]:
        print(DATETIME.series[i])

for i in range(len(BUY2.series)):
    if BUY2.series[i]:
        print(DATETIME.series[i])

# BUY = (B-B1 > 0) & (REF(B-B1, 1) < 0) & (COUNT(B-B1 < 0, 8) == 7)
# SELL = (B-B1 < 0) & (REF(B-B1, 1) > 0)



#买点
count = 10000
price = 0
# 0 为空仓 1为持仓
status = 0
for i in range(len(BUY)):
    #第一个转红的时候买入
    if BUY.series[i] and status == 0:
        status = 1
        price = CLOSE.series[i]
        print('在%s以%s元全仓买入' % (DATETIME.series[i], CLOSE.series[i]))
    #在第一个转绿的时候卖出
    if SELL.series[i] and status == 1:
        status = 0
        profit = round((CLOSE.series[i] - price) / price, 2)
        count = (profit + 1) * count
        print('在%s以%s元全仓卖出，本次交易盈利%s，当前账户余额%s元' % (DATETIME.series[i], CLOSE.series[i], str(profit * 100) + '%', count))



pass