# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/11 22:02
# FileName: demo_Softmax_classifier
# Description:  多分类问题

import torch
import numpy as np

# 输出一个分布

class MINISTDataset(torch.nn.Module):

    def __init__(self, filepath):
        xy = np.loadtxt(filepath, delimiter=',', dtype=np.float32)
        self.len = xy.shape[0]
        self.x = torch.from_numpy(xy[:, :-1])
        self.y = torch.from_numpy(xy[:, -1])

    def __getitem__(self, item):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.len

class Module(torch.nn.Module):

    def __init__(self):
        super(Module, self).__init__()
        self.linear1 = torch.nn.Linear(8, 6)
        self.linear2 = torch.nn.Linear(6, 4)
        self.linear3 = torch.nn.Linear(4, 1)
        self.sigmoid = torch.nn.Sigmoid()

    def forward(self, x):
        x = self.sigmoid(self.linear1(x))
        x = self.sigmoid(self.linear2(x))
        x = self.sigmoid(self.linear3(x))
        return x

model = Module()

criterion = torch.nn.BCELoss()
optimizer = torch.optim.SGD(model.parameters(), lr= .1)

for epoch in range(100):
    for i, data in enumerate(train_loader):
        inputs, label = data

        y_pred = model(inputs)
        loss = criterion(y_pred, y)
        print(epoch, loss)

        optimizer.zero_grad()
        loss.backward()

        optimizer.step()


print('loss and y_prd example'.center(100, '-'))
y = np.array([1, 0, 0])
z = np.array([.2, .1, -.1])
y_pred  =np.exp(z) / np.exp(z).sum()
loss = (-y  * np.exp(y_pred)).sum()
print(loss)

# 在torch中神经网络的最后一层不要做非线性变换(激活)
# 直接传给交叉熵损失计算即可

print("""交叉熵损失处理的时候注意事项
        1、y 需要是一个长整型的张量--LongTensor
        2、criterion = torch.nn.CrossEntropyLoss(),loss = critersion(z,y)
        """)

print('Example'.center(100, '-'))
criterion = torch.nn.CrossEntropyLoss()
y = torch.LongTensor([2, 0, 1])

y_pred1 = torch.Tensor([[0.1, 0.2, 0.9],
                        [1.1, 0.1, 0.2],
                        [0.2, 2.1, 0.1]])

y_pred2 = torch.Tensor([[0.8, 0.2, 0.3],
                        [0.2, 0.3, 0.5],
                        [0.2, 0.2, 0.5]])

l1 = criterion(y_pred1, y)
l2 = criterion(y_pred2, y)
print('Batch Loss1 = ', l1.data,
      '\nBatch Loss2 = ', l2.data)
# https://pytorch.org/docs/stable/nn.html
# CrossEntropyLoss与nllloss的区别
# why CrossEntropyLoss < == > LogSoftmax + NLLLoss
