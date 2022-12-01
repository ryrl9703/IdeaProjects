# coding: utf-8
# Author: ryrl
# CreateTime: 2022/1/9 20:44
# FileName: Linear_regression
# Description: linear regression by pytorch
'''
1、 prepare dataset:
2、 design model using Class: inherit from nn.Module
3、 Construct loss and optimizer: using pytorch API
4、 Training cycle: forward, backward, update
'''

import torch

print('Prepare dataset'.center(100, '='))
x_data = torch.Tensor([[1.0], [2.0], [3.0]])
y_data = torch.Tensor([[2.0], [4.0], [6.0]])

print('Design module'.center(100, '='))


class LinearModel(
    torch.nn.Module):  # usually define the module as a Class, it makes the module easy to develop in the future
    """
    module可以自动识别计算图并实现backward过程

    """

    def __init__(self):  # 构造函数；初始化对象的时候所调用的函数
        super(LinearModel, self).__init__()  # 调用父类的构造，必须有
        self.linear = torch.nn.Linear(1, 1)  # 利用pytorch中的一个类：Linear,包含了weight(w) and bias(b)，构造一个对象

    def forward(self, x):  # 前馈计算函数,必须要有；module会自动实现backward的过程，不需要再写
        y_pred = self.linear(x)  # 在一个对象(self.linear)后面加了括号，意味着实现了一个'''可调用的对象'''
        return y_pred


model = LinearModel()  # 实例化

print('Construct Loss and Optimizer'.center(100, '='))

criterion = torch.nn.MSELoss(size_average=False)
optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
