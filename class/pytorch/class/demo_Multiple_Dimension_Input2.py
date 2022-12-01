# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/10 4:09
# FileName: demo_Multiple_Dimension_Input2
# Description:


import torch

class Module(torch.nn.Module):

    def __init__(self):
        super(Module, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.sigmoid = torch.nn.Sigmoid()  # 调用sigmoid模块,作为一层;用来做计算图

    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x

model = Module()

critersion = torch.nn.BCELoss(size_average=False)
optimizer  = torch.optim.SGD(model.parameters(), lr= .1)


for epoch in range(100):
    # forward
    y_pred = model(x)  # 没有进行min-batch,下一讲
    loss = critersion(y_pred, y)
    print(epoch, loss.item())

    # Backward
    optimizer.zero_grad()
    loss.backward()

    # Update
    optimizer.step()