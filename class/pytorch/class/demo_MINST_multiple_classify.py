# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/11 23:38
# FileName: demo_MINST_multiple_classify
# Description:


import torch
from torchvision import transforms
from torchvision import datasets
from torch.utils.data import DataLoader
import torch.nn.functional as tf
import torch.optim as optim


print('Prepare dataset'.center(100, '-'))
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


print('Design Model'.center(100, '-'))

class Net(torch.nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.linear1 = torch.nn.Linear(784, 512)
        self.linear2 = torch.nn.Linear(512, 256)
        self.linear3 = torch.nn.Linear(256, 128)
        self.linear4 = torch.nn.Linear(128, 64)
        self.linear5 = torch.nn.Linear(64, 10)

    def forward(self, x):
        x = x.view(-1, 784)  # 将张量变成二阶(-1,列数)-1表示自动计算
        x = tf.relu(self.linear1(x))
        x = tf.relu(self.linear2(x))
        x = tf.relu(self.linear3(x))
        x = tf.relu(self.linear4(x))
        # x = tf.relu(self.linear5(x))  # 最后一层不要激活,交给Softmax
        return self.linear5(x)

model = Net()

print('criterion and optimizer'.center(100, '-'))
criterion = torch.nn.CrossEntropyLoss()  # 使用交叉熵损失
optimizer = optim.SGD(model.parameters(),
                      lr= .01, # 学习率
                      momentum= .5)  # 冲量值，优化训练过程

print('Training cycle'.center(100, '-'))
# 每次有训练又测试,写起来不好写
# 可以将每一轮循环封装成一个函数

def train(epoch):
    running_loss = 0.0
    for batch_index, data in enumerate(train_loader, 0):
        inputs, target = data  # x,y
        optimizer.zero_grad()

        # forward + backward + update
        output = model(inputs)
        loss = criterion(output, target)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()
        if batch_index % 300 == 299:  # 每300次输出一次running_loss
            print('[%d, %5d] loss: %3f' % (epoch + 1,
                                           batch_index + 1,
                                           running_loss / 300))
            running_loss = 0.0  # 重置

def test():  # 不需要计算梯度
    correct = 0
    total = 0
    with torch.no_grad():  # 此时，下面的代码不再计算梯度
        for data in test_loader:  # 拿数据
            images, labels = data
            outputs = model(images)  # 做预测
            _, predicted = torch.max(outputs.data, dim=1)  # dim=1沿着行去找最大值的下标
            total += labels.size(0)
            correct += (predicted == labels).sum().item()  # 计算猜对的个数
    print('Accurancy on test set: %d %%' % (100 * correct / total))

if __name__ == '__main__':
    for epoch in range(10):  # times进行多少轮
        train(epoch)
        test()

# Dataset: https://www.kaggle.com/c/otto-group-product-classification-challenge/data