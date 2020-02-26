# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
通达信所有函数
"""
import numpy as np

from core import NumericSeries


### 初始化基本变量
from funcs.api import *

for name in ["open", "high", "low", "close", "volume", "amount", "datetime"]:
    dtype = np.float64 if name != "datetime" else np.uint64
    cls = type("{}Series".format(name.capitalize()), (NumericSeries, ), {"name": name, "dtype": dtype})
    # obj = cls(dynamic_update=True)
    for var in [name[0], name[0].upper(), name.upper()]:
        globals()[var] = cls()

VOL = VOLUME
REF = ref
MIN = minimum
MAX = maximum
COUNT = count
EVERY = every
LLV = llv
HHV = hhv
IF = iif
CROSS = cross
ZIG = zig
BARSLAST = barslast


__all__ = [
    "OPEN", "O",
    "HIGH", "H",
    "LOW", "L",
    "CLOSE", "C",
    "VOLUME", "V", "VOL",
    "DATETIME",
    "AMOUNT",
]