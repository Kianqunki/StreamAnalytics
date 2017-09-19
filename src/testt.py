import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
from numpy import trapz
from scipy.integrate import simps
import math
from scipy.interpolate import spline
import random

a = np.random.lognormal(0.5, 1, 1000)
# a = sorted(a, reverse=True)
# plt.plot(a)
# plt.show()
# df = pd.DataFrame()
# df["a"] = a
# print df["a"].describe() 

# print np.percentile(range(0,11), range(10,110,10), interpolation='midpoint')
# print stats.percentileofscore(range(0,11), 6, kind='mean')

b = [0.30, 0.25, 0.15, 0.10, 0.05, 0.03, 0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.00]
c = [0.70, 0.20, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
d = [0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
e = [0.90, 0.10, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
f = [0.99, 0.01, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00]
g = [0.05 for i in range(1,21)]



def score(values):
    scoreg = values[0]
    for idx, i in enumerate(values):
        scoreg = scoreg / (1/(1-(values[idx]-values[idx+1])))
        if idx == 4:
            break
    return scoreg

# print score(b), score(c), score(d), score(e), score(f), score(g)
print score(c)

# w1 = [math.pow(0.8, i) for i in range(1, 21)]
# w2 = [math.pow(0.8, i*i) for i in range(1, 21)]
# w3 = [math.pow(0.8, i*i*i) for i in range(1, 21)]
# w4 = [0.5+random.randint(0,1)*0.01 for i in range(1, 21)]

# print score(w1), score(w2), score(w3), score(w4)


# # b2 = [0.4, 0.3, 0.2, 0.1]
# # c2 = [0.8, 0.1, 0.075, 0.025]
# # d2 = [0.25, 0.25, 0.25, 0.25]

# # print trapz(b), trapz(c), trapz(d)
# # print simps(b2), trapz(c2), trapz(d2)

# # ps = []
# # for i in d: 
# #     ps.append(stats.percentileofscore(b, i))

# # print ps

# # sum = 0
# # for idx, i in enumerate(b):
# #     sum += math.pow(1/(1-i), math.pow(idx + 1, 2))
# # print sum

# # sum = 0
# # for idx, i in enumerate(c):
# #     sum += math.pow(1/(1-i), math.pow(idx + 1, 2))
# # print sum

# # sum = 0
# # for idx, i in enumerate(d):
# #     sum += math.pow(1/(1-i), math.pow(idx + 1, 2))
# # print sum

# # b1 = list(b)
# # c1 = list(c)
# # d1 = list(d)

# # for idx, i in enumerate(b):
# #     b1[idx] = -math.log10(i+0.0001)

# # for idx, i in enumerate(c):
# #     c1[idx] = -math.log10(i+0.0001)

# # for idx, i in enumerate(d):
# #     d1[idx] = -math.log10(i+0.0001)

# # print trapz(b1), trapz(c1), trapz(d1)

# # plt.plot(b, c="b")
# # plt.plot(c, c="r")
# # plt.plot(d, c="g")
# # plt.show()

# # plt.plot(b1, c="b")
# # plt.plot(c1, c="r")
# # plt.plot(d1, c="g")
# # plt.show()


# wn1 = list(w1)
# wn2 = list(w2)
# wn3 = list(w3)
# wn4 = list(w4)

# for idx, i in enumerate(w1):
#     wn1[idx] = -math.log10(i+0.0001)

# for idx, i in enumerate(w2):
#     wn2[idx] = -math.log10(i+0.0001)

# for idx, i in enumerate(w3):
#     wn3[idx] = -math.log10(i+0.0001)

# for idx, i in enumerate(w4):
#     wn4[idx] = -math.log10(i+0.0001)

# print trapz(wn1), trapz(wn2), trapz(wn3), trapz(wn4)

# plt.plot(w1, c="b")
# plt.plot(w2, c="r")
# plt.plot(w3, c="g")
# plt.plot(w4, c="c")
# plt.show()

# plt.plot(wn1, c="b")
# plt.plot(wn2, c="r")
# plt.plot(wn3, c="g")
# plt.plot(wn4, c="c")
# plt.show()