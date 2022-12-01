# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/9 18:09
# FileName: demo_Tensors
# Description:


import torch
import numpy as np

print('Initializing a Tensor'.center(100, '-'))
# Tensors can be initialized in various ways

# Directly from data
data = [[1, 2], [3, 4]]
x_data = torch.Tensor(data)

# from a numpy array
np_array = np.array(data)
x_np = torch.from_numpy(np_array)

# from another tensor
x_ones = torch.ones_like(x_data)  # size and shape is like x_data but all one
x_rand = torch.rand_like(x_data, dtype= torch.float)


print('Attributes of a Tensor'.center(100, '-'))
# Tensor attributes describe their shape, dtype, and the device on which they are stored
tensor = torch.rand(3, 4)
print('shape of tensor: %s' % {tensor.shape})
print('datatype of tensor: %s' % {tensor.dtype})
print('device tensor is stored on: %s' % {tensor.device})


print('Operations on Tensors'.center(100, '-'))
# if GPU is avilable, you can move the tensor to GPU like this:
if torch.cuda.is_available():
    tensor = tensor.to('cuda')
else:
    print('cuda is not avilable')

# if you are familiar with the numpy API, you will find tensor API is easy to use

# Standard numpy-like indexing and slicing
tensor = torch.ones(4, 4)
print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1]}")
tensor[:,1] = 0
print(tensor)
