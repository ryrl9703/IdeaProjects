# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/9 19:40
# FileName: demo_Logistic_regression
# Description: 分类问题, 输出的是概率

import torch
import torchvision
import torch.nn.functional as tf

train_set = torchvision.datasets.MNIST(root= '/public/workspace/ryrl/remote/projects/study/pytorch/data', download=True)
test_set  = torchvision.datasets.MNIST(root='/public/workspace/ryrl/remote/projects/study/pytorch/data', train=False, download=True)
# torchvision.datasets.CIFAR10()

print('二分类'.center(100, '-'))  # 最终计算p(fail) and p(pass)
# 饱和函数

print('Prepare data'.center(100, '-'))
x = torch.Tensor([[1.0], [2.0], [3.0]])
y = torch.Tensor([[0], [0], [1]])

print('Design model using class'.center(100, '-'))
class LogisticRegressionModel(torch.nn.Module):
    def __init__(self):
        super(LogisticRegressionModel, self).__init__()
        self.linear = torch.nn.Linear(1,1)  # (输入维度, 输出维度)

    def forward(self, x):
        y_pred = tf.sigmoid(self.linear(x))  # 线型变换后的结果多为变量传入sigmoid,进行非线性变换
        return y_pred

model = LogisticRegressionModel()

print('Contruct loss and optimizer'.center(100, '-'))
criterion = torch.nn.BCELoss(size_average= False)
optimizer = torch.optim.SGD(model.parameters(), lr= .01)

print('Training cycle'.center(100, '-'))
for epoch in range(100):
    y_pred = model(x)
    loss = criterion(y_pred, y)
    print(epoch, loss.item())

    optimizer.zero_grad()
    loss.backward()

    optimizer.step()


# import numpy as np
# import matplotlib.pyplot as plt
#
# x_l = np.linspace(0, 10, 200)
# x_t = torch.Tensor(x_l).view(200,1)
# y_t = model(x_t)
# y  = y_t.data.numpy()
# plt.plot(x, y)
# plt.plot([0, 10], [.5, .5], c = 'r')
# plt.xlabel('hours')
# plt.ylabel('probability of pass')
# plt.grid()
# plt.show()