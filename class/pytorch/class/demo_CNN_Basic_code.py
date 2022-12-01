# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/13 0:10
# FileName: demo_CNN_Basic_code
# Description:

import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as tf
import torch.optim as optim

print('A Simple Convolutional Neural Network'.center(100, '-'))

batch_size = 64
transform = transforms.Compose([  # 里面的操作按顺序执行
    transforms.ToTensor(),  # 将图片信息转化为Tensor
    transforms.Normalize((0.1307,), (0.3081,))  # 标准化; (均值,), (标准差,)
])  # 把原始图像转变为图像张量,像素值[0,1]

train_dataset = datasets.MNIST(root='./data/MNIST/',
                               train=True,
                               download=True,
                               transform=transform)

train_loader = DataLoader(train_dataset,
                          shuffle=True,
                          batch_size=batch_size)

test_dataset = datasets.MNIST(root='./data/MNIST/',
                              train=False,
                              download=False,
                              transform=transform)

test_loader = DataLoader(test_dataset,
                         shuffle=False,
                         batch_size=batch_size)


class Net(torch.nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.conv1 = torch.nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10, 20, kernel_size=5)  # 建立两个卷积层
        self.pooling = torch.nn.MaxPool2d(kernel_size=2)  # 池化层
        self.fc = torch.nn.Linear(320, 10)  # 全连接层

    def forward(self, x):
        # Flatten data from (n, 1,28,28) to (n, 784)
        batch_size = x.size(0)  # 计算batch size
        x = self.pooling(tf.relu(self.conv1(x)))
        x = self.pooling(tf.relu(self.conv2(x)))  # 卷积->池化->relu
        x = x.view(batch_size, -1)  # flatten
        x = self.fc(x)  # 最后一层不做激活(非线性变换)
        return x


model = Net()

# 如果要使用GPU
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model.to(device=device)

criterion = torch.nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=.01, momentum=.5)


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
