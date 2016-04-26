# Coding by SunChuan in 2016/04/26
import numpy as np
# data = range(1,10,1)
# print(data)
# arr = np.array(data)
# print(arr)


data = [1, 2, 3, 4]
print(data)
arr = np.array(data,dtype=np.int32)
print(arr)#注意两者之间的区别，一个变成了矩阵，一个还是list
print(arr.dtype)
print(arr.ndim)
print(arr.shape)
print(np.zeros((2,2)))
print(np.arange(1,10,2))

arr1 = np.random.randn(7,4)
arr2 = np.random.randn(4,7)
print(arr1)
print(arr2)
print(arr1@arr2)
