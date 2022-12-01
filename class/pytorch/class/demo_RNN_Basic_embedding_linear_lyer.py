# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/16 0:23
# FileName: demo_RNN_Basic_embedding_linear_lyer
# Description:


import torch

num_class = 4
input_size = 4
hidden_size = 8
embedding_size = 10
num_layers = 2
batch_size = 1
seq_len = 5


idx2chr = ['e', 'h', 'l', 'o']
x_data = [1,0,2,2,3]  # (batch, seqLen)
y_data = [3,1,2,3,2]  # (batch * seqLen)

inputs = torch.LongTensor(x_data).view(batch_size, seq_len)
labels = torch.LongTensor(y_data)

class Module(torch.nn.Module):

    def __init__(self):
        super(Module, self).__init__()
        self.emb = torch.nn.Embedding(input_size, embedding_size)  # 嵌入层;(input_size, embedding_size)构成矩阵
        self.rnn = torch.nn.RNN(input_size=embedding_size,  # longTensor:(baychsize, seqLen)
                                hidden_size=hidden_size,
                                num_layers=num_layers,batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, num_class)  # 全连接层

    def forward(self, x):
        hidden = torch.zeros(num_layers, x.size(0), hidden_size)
        x = self.emb(x)  # (batch_size, seqLen, embeddingSize)
        x, _ = self.rnn(x, hidden)
        x = self.fc(x)
        return x.view(-1, num_class)  # 最后变成矩阵

model = Module()

criterion = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=.05)

for epoch in range(15):
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, labels)

    loss.backward()
    optimizer.step()

    _, idx = outputs.max(dim=1)
    idx = idx.data.numpy()
    print('Predicted:', ''.join([idx2chr[x] for x in idx]), end='')
    print(', Epoch [%d/15] loss = %.3f' % (epoch + 1, loss.item()))

# 阅读文档，了解LSTM
# https://pytorch.org/docs/stable/nn.html

# GRU
# 序列数据、循环过程使用的循环共享的机制