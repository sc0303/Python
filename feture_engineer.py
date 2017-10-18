from numpy import nan, array, vstack
from sklearn.datasets import load_iris
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.feature_selection import VarianceThreshold

import antigravity




iris = load_iris()

print(iris.target)

# 标准化
# StandardScaler().fit_transform(iris.data)

# MinMaxScaler.fit_transform(iris.data)

# 哑编码
# print(OneHotEncoder().fit_transform(iris.target.reshape((-1, 1))))

# 缺失数值计算
# print(Imputer().fit_transform(vstack((array([nan, nan, nan, nan]), iris.data))))

# 自动挑选方差大于3的样本作为模型的样本输入
print(VarianceThreshold(threshold = 3).fit_transform(iris.data))


