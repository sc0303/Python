# write on 2017/07/26 by Chuan.sun
import numpy as np
# 创建计算缓存，避免重复计算
from tempfile import mkdtemp
from shutil import rmtree
# 数据预处理
from numpy import hstack, vstack, array, nan,median
from numpy.random import choice
from scipy.stats import pearsonr
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import MaxAbsScaler
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import Binarizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import OneHotEncoder


# 缺失值计算
from sklearn.preprocessing import Imputer
from sklearn.preprocessing import PolynomialFeatures

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

# 交叉检验
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import RepeatedKFold
from sklearn.model_selection import LeaveOneOut
#
# # Caching transformers: avoid repeated computation
# # 创建缓存
# cachedir = mkdtemp()
# # pipeline中使用缓存
# pipe = Pipeline(estimators, memory=cachedir)
# # 删除缓存
# rmtree(cachedir)



# 特征选择
from sklearn.feature_selection import VarianceThreshold
from sklearn.feature_selection import SelectKBest
# 卡方检验
from sklearn.feature_selection import chi2
# 互信息法
from minepy import MINE
# Wrapper方法
from sklearn.feature_selection import RFE
# 基于惩罚项
from sklearn.feature_selection import SelectFromModel
# 基于树模型
from sklearn.ensemble import GradientBoostingClassifier

# 数据降维
# 主成份
from sklearn.decomposition import PCA
from sklearn.decomposition import KernelPCA
# 线性判别法
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# 串行、并行流水线
from sklearn.pipeline import Pipeline
from sklearn.pipeline import FeatureUnion

# 自动化调参
from sklearn.model_selection import GridSearchCV

# def mic(x, y):
#     m = MINE()
#     m.compute_score(x, y)
#     return (m.mic(), 0.5)



iris = datasets.load_iris()
# 数据标准化，是的数据符合状态分布


X_train,X_test,Y_train,Y_test = train_test_split(iris.data,iris.target,random_state=0,test_size=0.4)
print(X_train.shape)
print(X_test.shape)


data_standard = StandardScaler().fit_transform(iris.data)
data_minmax = MinMaxScaler().fit_transform(iris.data)
# print(iris.data[1:])
# Normalizer主要对变量进行行的归一化，其目的在于样本向量在点乘运算或其他核函数计算相似性时，拥有统一的标准，也就是说都转化为“单位向量”。
data_normalizer = Normalizer(norm='l1').fit_transform(iris.data)
data_normalizer2 = Normalizer(norm='l2').fit_transform(iris.data)
# data_binary = Binarizer(threshold=3).fit_transform(iris.data)
# data_one_hot = OneHotEncoder().fit_transform(iris.data)
# data_imputer = Imputer(strategy='mean').fit_transform(vstack((array([nan,nan,nan,nan]),iris.data)))
# poly_feature = PolynomialFeatures().fit_transform(iris.data)
# varianct_threshold = VarianceThreshold(threshold=2).fit_transform(iris.data)

# print(OneHotEncoder().fit_transform(iris.data[:1]))
print(data_normalizer)
print(data_normalizer2)

X_train = np.array([[ 1., -1.,  2.],
                   [ 2.,  0.,  0.],
                     [ 0.,  1., -1.]])

X_test = np.array([[ -3., -1.,  4.]])
# 使用训练节进行fit，得到的参数去transform测试集
min_max_scaler = MinMaxScaler()
print(min_max_scaler)
X_train_minmax = min_max_scaler.fit_transform(X_train)
print(min_max_scaler)
X_test_minmax = min_max_scaler.transform(X_test)
print(X_test_minmax)



X = np.array([[0., 0.], [1., 1.], [-1., -1.], [2., 2.]])
X_train = X[train]
print(X_train)

# 选择相关系数最大的2个feature
# select_kb = SelectKBest(lambda X,Y:array(list(map(lambda x: pearsonr(x,Y),X.T))).T[0],k = 2).fit_transform(iris.data,iris.target)
# print(select_kb)
# select_chi2 = SelectKBest(chi2,k = 2).fit_transform(iris.data,iris.target)
# print(select_chi2)
# select_mic = SelectKBest(lambda X,Y:array(list(map(lambda x: mic(x,Y),X.T))).T[0],k = 2).fit_transform(iris.data,iris.target)
# print(select_mic)

# wrapper = RFE(estimator=LogisticRegression(),n_features_to_select=2).fit_transform(iris.data,iris.target)
# print(wrapper)

# select_from_model = SelectFromModel(LogisticRegression(penalty='l1',C = 0.1)).fit_transform(iris.data,iris.target)
# print(select_from_model)

# gbdt_select = SelectFromModel(GradientBoostingClassifier()).fit_transform(iris.data,iris.target)
# print(gbdt_select)


# pca = PCA(n_components=2).fit_transform(iris.data)
# print(pca)

# lda = LinearDiscriminantAnalysis(n_components=2).fit_transform(iris.data,iris.target)
# print(lda)

# print(iris.data[0])
# print(VarianceThreshold(threshold=2).fit_transform(iris.data)[0])

# print(data_standard)
# print(data_minmax)
# print(data_normalizer)
# print(data_binary)
# print(data_one_hot)
# print(data_imputer)
# print(poly_feature)


# print(StandardScaler().fit_transform(array([1,2])))
# print(Normalizer().fit_transform(array([1,2])))
# list = Normalizer().fit_transform(array([1,2]))
# print(list[0][0]**2+list[0][1]**2)


# pipeline
# estimators = [('pca',PCA()),('clf',LogisticRegression())]
# pipe = Pipeline(estimators)
# print(pipe)
# print(pipe.steps[0])
# print(pipe.named_steps['pca'])
# print(pipe.set_params(clf__C = 10))
# params = dict(pca__n_components = [2,5,10],clf__C = [0,1,10,100])
# 非最后一步，可以通过None忽略是否需要该步骤
# params2 = dict(pca = [None,PCA(5),PCA(10)],clf = [SVC(),LogisticRegression()],clf__C = [0.1,10,100])
# grid_research = GridSearchCV(pipe,param_grid=params)
# make_pipeline(Binarizer(),MultinomialNB())





# estimators=[('reduce_dim',PCA()),('clf',SVC())]#其中的'reduce_dim'是自定义的步骤名字
# pipe=Pipeline(estimators)
# make_pipeline(Binarizer(),MultinomialNB())#make_pipeline是上面代码的一种简写形式
# pipe.steps[0]#steps属性里以列表形式存着管道中的估计器
# pipe.named_steps['reduce_dim']#在named_steps属性中以dict形式存着步骤
# pipe.set_params(clf__C=10)#以这种形式给指定名字的估计器（clf）的参数（C)赋值 <estimator>__<parameter>
# params=dict(reduce_dim__n_components=[2,5,10],#设置reduce_dim的n_components参数为多个值以供选取模型最优值
#             clf__C=[0.1,10,100])#在模型选择过程中可以设置参数列表
# grid_search=GridSearchCV(pipe,param_grid=params)
#
# params=dict(reduce_dim=[None,PCA(5),PCA(10)],clf=[SVC(),LogisticRegression()],clf__C=[0.1,10,100])
# grid_search=GridSearchCV(pipe,param_grid=params)
#


# featureunion
# estimators_union = [('linear_pca',PCA()),('kernel_pca',KernelPCA)]
# combined = FeatureUnion(estimators_union)
# print(combined)


# estimators=[('linear_pca',PCA()),('kernel_pca',KernelPCA())]
# combined=FeatureUnion(estimators)
# combined.set_params(kernel_pca=None)#Pipeline一样，可以使用set_params替换单独的步骤，并通过设置为None来忽略




# print(OneHotEncoder().fit_transform([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]]).toarray())
# print(OneHotEncoder().fit([[0, 0, 3], [1, 1, 0], [0, 2, 1], [1, 0, 2]]).transform([[0, 1, 3]]).toarray())

# 随机选取数字
# iris.data = hstack((choice([0, 1, 2], size=iris.data.shape[0] + 1).reshape(-1, 1),
#                     vstack((iris.data, array([nan, nan, nan, nan]).reshape(1, -1)))))

# print(median(iris.target))

# print(hstack((iris.target,array([median(iris.target)]))))



# iris = datasets.load_iris()
#
# digits = iris.data
# targets = iris.target.reshape((-1,1))
#
# # 数据标准化，标准化成正态分布
# digits_standard = StandardScaler().fit_transform(digits)
# # 数据区间缩放
# digits_minmax = MinMaxScaler().fit_transform(digits)
# # 数据归一化
# digits_normalize = Normalizer().fit_transform(digits)
# # 数据二值化
# digits_binary = Binarizer(threshold=3).fit_transform(digits)
# # 哑变量编码
# targets_onehot = OneHotEncoder().fit_transform(targets)
#
# print(targets)
#
# print(targets_onehot)
