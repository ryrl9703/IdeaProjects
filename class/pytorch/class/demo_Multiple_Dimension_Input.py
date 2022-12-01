# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/10 3:35
# FileName: demo_Multiple_Dimension_Input
# Description:

import torch
import numpy as np



class Module(torch.nn.Module):

    def __init__(self):
        super(Module, self).__init__()
        self.linear = torch.nn.Linear(8, 1)  # 这次输入数据是一个八维数据，输出一维的数据;八维的空间映射到一维的空间
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.linear(x))
        return x

model = Module()

"""
Logistic Regression是只有一层的神经网络；
把多个Logistic Regression回归首尾相连便可以形成一个多层的神经网络
"""

