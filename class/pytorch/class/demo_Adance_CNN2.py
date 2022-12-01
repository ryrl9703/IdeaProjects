# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/14 22:05
# FileName: demo_Adance_CNN2
# Description:

import os
import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as tf
import torch.optim as optim

os.chdir('/public/workspace/ryrl/remote/projects/study/pytorch')
batch_size = 64
transform = transforms.Compose([  # 里面的操作按顺序执行
    transforms.ToTensor(),  # 将图片信息转化为Tensor
    transforms.Normalize((0.1307, ), (0.3081, ))  # 标准化; (均值,), (标准差,)
])  # 把原始图像转变为图像张量,像素值[0,1]

train_dataset = datasets.MNIST(root='./data/MNIST/',
                               train=True,
                               download=True,
                               transform=transform)

train_loader = DataLoader(train_dataset,
                          shuffle= True,
                          batch_size=batch_size)

test_dataset = datasets.MNIST(root='./data/MNIST/',
                              train=False,
                              download=False,
                              transform=transform)

test_loader = DataLoader(test_dataset,
                         shuffle= False,
                         batch_size=batch_size)


class ResidualBlock(torch.nn.Module):  # 输出和输入的通道数要保持一致;有多中实现方式

    def __init__(self, channels):
        super(ResidualBlock, self).__init__()
        self.channels = channels
        self.conv1 = torch.nn.Conv2d(in_channels=channels,
                                     out_channels=channels,
                                     kernel_size=3, padding=1)

        self.conv2 = torch.nn.Conv2d(in_channels=channels,
                                     out_channels=channels,
                                     kernel_size=3, padding=1)

    def forward(self, x):
        y = tf.relu(self.conv1(x))
        y = self.conv2(y)  # 最后一层不激活
        return tf.relu(x + y)  # 先求和再激活

class Net(torch.nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 16, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(16, 32, kernel_size=5)
        self.mp = torch.nn.MaxPool2d(2)

        self.rblock1 = ResidualBlock(16)
        self.rblock2 = ResidualBlock(32)

        self.fc = torch.nn.Linear(512, 10)

    def forward(self, x):
        in_size = x.size(0)
        x = self.mp(tf.relu(self.conv1(x)))
        x = self.rblock1(x)
        x = self.mp(tf.relu(self.conv2(x)))
        x = self.rblock2(x)
        x = x.view(in_size, -1)
        x = self.fc(x)
        return x

model = Net()

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.SGD(model.parameters(), lr=.01, momentum= .5)


def train(epoch):
    running_loss = 0.0
    for batch_index, data in enumerate(train_loader):
        inputs, target = data
        # inputs, target = inputs.to(device), target.to(device)  # 数据模型要放到一块显卡上
        optimizer.zero_grad()

        output = model(inputs)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_index % 300 == 299:
            print('[%d, %5d] loss: %3f' % (epoch + 1,
                                           batch_index + 1,
                                           running_loss / 300))
            running_loss = 0.0

def test():
    correct = 0
    total = 0
    with torch.no_grad():
        for data in test_loader:
            images, labels = data
            # inputs, target = inputs.to(device), target.to(device)
            output = model(images)
            _, predicted = torch.max(output.data, dim=1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()  # 计算猜对的个数
    print('Accurancy on test set: %d %%' % (100 * correct / total))

if __name__ == '__main__':
    for epoch in range(10):
        train(epoch)
        test()