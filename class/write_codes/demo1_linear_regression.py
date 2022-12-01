# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/13 19:22
# FileName: demo1_linear_regression
# Description:

import torch

x = torch.Tensor([[1.0], [2.0], [3.0]])
y = torch.Tensor([[2.0], [4.0], [6.0]])

class LinearModel(torch.nn.Module):

    def __init__(self):
        super(LinearModel, self).__init__()
        self.linear = torch.nn.Linear(1, 1)

    def forward(self, x):
        y_pred = self.linear(x)
        return y_pred

model = LinearModel()

criterion = torch.nn.MSELoss(size_average=False)
optimizer = torch.optim.SGD(model.parameters(), lr= 0.01)

for epoch in range(10):
    y_pred = model(x)
    loss = criterion(y_pred, y)

    optimizer.zero_grad()
    loss.backward()

    optimizer.step()