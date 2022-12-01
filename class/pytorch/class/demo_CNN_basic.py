# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/12 22:14
# FileName: demo_CNN_basic
# Description: Convolutional Neural Network

import torch


# 线型层全连接输入值和每一个输出值都有一个权重，每一个输入值都参与全部的计算过程

print('Convolutional Layer'.center(100, '-'))
in_channels, out_channels = 5, 10
width, height = 100, 100
kernel_size = 3  # 卷积核的大小
batch_size = 1

inputs = torch.randn(batch_size,
                     in_channels,
                     width,
                     height)

conv_layer = torch.nn.Conv2d(in_channels,
                             out_channels,
                             kernel_size=kernel_size)

output = conv_layer(inputs)

print(inputs.shape)
print(output.shape)
print(conv_layer.weight.shape)

print('Padding'.center(100, '-'))
# 如果想要卷积之后图像大小不变，可以在图像外面添加padding
# 要添加几个padding，可以用卷积核大小整除2来计算

inputs = [3,4,5,6,7,
          2,4,6,8,2,
          1,6,7,8,4,
          9,7,4,6,2,
          3,7,5,4,1]

inputs = torch.Tensor(inputs).view(1, 1, 5, 5)  # (batch_size, channel, width, height)
conv_layer = torch.nn.Conv2d(1, 1,  # 输入通道，输出通道
                             kernel_size=3,
                             padding=1,
                             bias=False)

kernel = torch.Tensor([1,2,3,4,5,6,7,8,9]).view(1,1,3,3)  # 构造卷积核.(output, input, width, height)
conv_layer.weight.data = kernel.data

output = conv_layer(inputs)
print(output)

print('Stride'.center(100, '-'))
# 卷积核核心移动的步长, 可以有效的缩小图像

print('Max Pooling Layer'.center(100, '-'))
# 下采样方法：最大池化
# 通道不变，图像大小会变(减半)

inputs = [3,4,6,5,
          2,4,6,8,
          1,6,7,8,
          9,7,4,6]
inputs = torch.Tensor(inputs).view(1, 1, 4, 4)
maxpooling_layer = torch.nn.MaxPool2d(kernel_size=2)
output = maxpooling_layer(inputs)
print(output)
