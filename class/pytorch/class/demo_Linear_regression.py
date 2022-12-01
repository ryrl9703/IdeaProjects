# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/8 22:07
# FileName: demo1
# Description:


import numpy as np
import pandas as pd
import torch

x = torch.Tensor([[1.0], [2.0], [3.0]])
y = torch.Tensor([[2.0], [4.0], [6.0]])  # y = wx + b

# pytorch中的重点是构造计算图，通过x，y矩阵的阶数确定w，b的阶数

class LinearModel(torch.nn.Module):  # 构造模型的模板，CNN，多层感知机，全连接的神经网络，RNN等通用;全部继承子module这个模块

    def __init__(self):  # 构造函数
        super(LinearModel, self).__init__()  # super调用父类的构造,每次记得抄上去就行，必须有
        self.linear = torch.nn.Linear(1,1)  # nn.Linear是pytorch中的一个类,在一个类后面加括号就是在构造一个对象

    def forward(self, x):  # 前馈过程中使用的计算; module模块会根据你的计算图自动实现backward
        y_pred = self.linear(x)  # 进行的操作是：w * x + b
        return y_pred

model = LinearModel()  # 实例化; 可直接调用


print('损失函数和优化器'.center(100, '-'))
criterion = torch.nn.MSELoss(size_average= False)  # 计算损失
optimizer = torch.optim.SGD(model.parameters(), lr= .01)  # lr学习率; 优化器对象; 有很多的优化器可以选择、尝试

print('训练过程'.center(100, '-'))

for epoch in range(100):
    y_pred = model(x)  # 计算理论值
    loss   = criterion(y_pred, y)  # 计算损失值
    print(epoch, loss)  # 每次训练输出训练次数，和损失值

    optimizer.zero_grad()  # 梯度归零
    loss.backward()  # 反向传播
    optimizer.step()  # 更新

print('w = ', model.linear.weight.item())
print('b = ', model.linear.bias.item())


x_test = torch.Tensor([[4.0]])
y_test = model(x_test)
print('y_pred = ', y_test.data)

"""
需要注意：
    对于训练集随着训练的次数增加，损失会越来越少
    但是对于开发集，随着训练的次数增多，损失会先减少后增加，所以训练次数并不是越多越好
"""