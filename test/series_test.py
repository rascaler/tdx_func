from tdx_func.core import NumericSeries
import numpy as np


n1 = NumericSeries(np.array([1, 2]))
n2 = NumericSeries(np.array([3, 4]))
print("aaa:%s" % (n1 + n2).series)
print("aaa:%s" % (n1 > n2))

print(np.array([3, 4]) > 4)

print((4 + n1).series)