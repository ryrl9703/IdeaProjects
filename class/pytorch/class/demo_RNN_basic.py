# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/15 23:48
# FileName: demo_RNN_basic
# Description:

import torch

input_size = 4
hidden_size = 4
batch_size = 1
num_layers = 1

idx2chr = ['e', 'h', 'l', 'o']
x_data = [1, 0, 2, 2, 3]
y_data = [3, 1, 2, 3, 2]

one_hot_lookup = [[1,0,0,0],
                  [0,1,0,0],
                  [0,0,1,0],
                  [0,0,0,1]]

x_one_hot = [one_hot_lookup[x] for x in x_data]

inputs = torch.Tensor(x_one_hot).view(-1, batch_size, input_size)
labels = torch.LongTensor(y_data)  # shape of labels: (seqLen * batchsize,1)

class Module(torch.nn.Module):

    def __init__(self, input_size, hidden_size, batch_size, num_layers=1):
        super(Module, self).__init__()
        self.num_layers = num_layers
        self.batch_size = batch_size  # 构造隐层里面的h(0)
        self.input_size = input_size
        self.hidden_size = hidden_size

        self.rnn = torch.nn.RNN(input_size=self.input_size,
                                hidden_size=self.hidden_size,
                                num_layers=num_layers)

    def forward(self, input):
        hidden = torch.zeros(self.num_layers,
                             self.batch_size,
                             self.hidden_size)  # 隐层的维度:num_layer * batch_size * hidden_size
        out, _ =self.rnn(input, hidden)
        return out.view(-1, self.hidden_size)  # 改变输出的维度:(seqLen * batch_size,hidden_size);2维度？？？;好处是:使用交叉熵的时候变成矩阵了
model = Module(input_size=input_size, hidden_size=hidden_size, batch_size=batch_size, num_layers=num_layers)

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=.5)

for epoch in range(15):
    optimizer.zero_grad()
    output = model(inputs)
    loss = criterion(output, labels)

    loss.backward()
    optimizer.step()

    _, idx = output.max(dim=1)
    idx = idx.data.numpy()
    print('Predicted:', ''.join([idx2chr[x] for x in idx]), end='')
    print(', Epoch [%d/15] loss = %.3f' % (epoch + 1, loss.item()))

"""
处理自然语言的时候，独热向量的缺点：
    1、维度太高：字母级别(128),词级别(......)
    2、向量过于稀疏
    3、硬编码,不是学习出来的

希望达到的目的：
    1、低纬度
    2、稠密
    3、从数据中学习
A popular and powerfil way is called EMBEDDING(嵌入层)  # 把高纬度的稀疏的样本映射到稠密的低纬度的空间--> 数据的降维
Embed 的输入层必需是一个长整型的张量
"""
