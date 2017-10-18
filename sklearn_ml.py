# Write on 2017/08/24 by Chuan.sun
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Perceptron
from sklearn.linear_model.ridge import  RidgeCV
from sklearn.linear_model.coordinate_descent import LassoCV

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.datasets import  load_iris
import plotly.plotly as py
import plotly.graph_objs as go
from sklearn.metrics.pairwise import cosine_similarity


class Person:
    def __init__(self):
        pass

    def getAge(self):
        print (__name__)

p = Person()
p.getAge()



# 线性回归
# reg=LinearRegression(copy_X=True, fit_intercept=True, n_jobs=1, normalize=False).fit([[0, 0], [1, 1], [2, 2]], [0, 1, 2])
# print(reg.coef_)
# print(reg.intercept_)

# data_set = pd.DataFrame(np.array([[0, 0],[1, 1],[2, 2]]),columns=['x','y'])
# trace0 = go.Scatter(
#     x = data_set['x'],
#     y = data_set['y'],
#     name = '样本分布',
#     line = dict(
#         color = ('rgb(205, 12, 24)'),
#         width = 4)
# )
# data = [trace0]
#
# py.iplot(data, filename='basic-line')




#
#
# sns.lmplot(x="x", y="y", data=data_set)
# sns.plt.show()
# sns.plt.close()
#
# # 岭回归 一阶范数
# lasso_cv = LassoCV(alphas=[0.1,1.0,10],cv =None,fit_intercept=True,normalize=False).fit([[0,0],[0,0],[1,1]],[0,.1,1])
# print(lasso_cv.coef_)
# print(lasso_cv.alpha_)
#
# # 岭回归 二阶范数
# reg_ridge_cv = RidgeCV(alphas=[0.1,1.0,10],cv =None,fit_intercept=True,scoring=None,normalize=False).fit([[0,0],[0,0],[1,1]],[0,.1,1])
# print(reg_ridge_cv.coef_)
# print(reg_ridge_cv.alpha_)