# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/11 0:16
# FileName: demo_Dataset_DataLoader
# Description:

import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset  # dataset is an abstract class,抽象类，不能实例化，只能被子类继承
from torch.utils.data import DataLoader  # 加载数据用，可以实例化

"""
# Training cycle
for epoch in range(training_epochs):  # 外层循环周期
    # Loop over all batches
    for i in range(total_batch):  # mini-batch 内层对batch进行迭代
"""

# epoch: 所有的训练样本都进行了一次前馈和反馈，便称为一个epoch
# Batch-size: 进行一次前馈和一次反馈所用的样本数量
# iteration: 迭代次数



print('Prepare dataset'.center(100, '-'))
class DiabetesDataset(DataLoader):  # DiabetesDataset类继承自Dataset
    def __init__(self, filepath):  # 都读进内存中或者打包成小的文件
        super(DiabetesDataset, self).__init__()
        xy = np.loadtxt(filepath, delimiter=',', dtype=np.float32)
        sel.len = xy.shape[0]
        self.x = torch.from_numpy(xy[:, :-1])
        self.y = torch.from_numpy(xy[:, [-1]])

    def __getitem__(self, index):  # 使实例化的对象能够支持下标操作
        return self.x[index], self.y[index]

    def __len__(self):  # 使其能返回数据条数
        return self.len

dataset = DiabetesDataset()  # 实例化
train_loader = DataLoader(dataset=dataset,
                          batch_size= 32,
                          shuffle=True,
                          num_workers=2)  # 至少指定这几个参数

print('Design model using class'.center(100, '-'))
class Module(torch.nn.Module):

    def __init__(self):
        super(Module, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self,x):
        x = self.sigmoid(self.linear1(x))
        x=  self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x

model = Module()

print('criterion an optimizer'.center(100, '-'))
criterion = torch.nn.BCELoss(size_average= False)
optimizer = torch.optim.SGD(model.parameters(), lr= .1)

print('Training cycle'.center(100, '-'))
for epoch in range(100):  # 变成了嵌套循环
    for i, data in enumerate(train_loader):
        # 1、Prepare data
        inputs, labels = data

        # 2、Forward
        y_pred = model(inputs)
        loss = criterion(y_pred, labels)
        print(epoch, i, loss.item())

        # 3、Backward
        optimizer.zero_grad()
        loss.backward()

        # Update
        optimizer.step()

# https://www.kaggle.com/c/titanic/data