# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/16 0:57
# FileName: demo_RNN_Classifier
# Description: 循环神经网络分类器

import csv
import gzip
import math
import time

import torch
import numpy as np
import matplotlib.pylab as plt
from torch.utils.data import Dataset
from torch.utils.data import DataLoader

def time_since(since):
    s = time.time() - since
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

print('Convert name to tensor'.center(100, '-'))

def create_tensor(tensor):
    if use_GPU:
        device = torch.device('cuda:0')
        tensor = tensor.to(device)
    return tensor

def make_tensor(names, countries):
    sequences_and_lengths = [name2list(name) for name in names]
    name_sequences = [sl[0] for sl in sequences_and_lengths]
    seq_lengths = torch.LongTensor([sl[1] for sl in sequences_and_lengths])
    countries = countries.long()

    # make tensor of name, batchSize x SeqLen
    seq_tensor = torch.zeros(len(name_sequences), seq_lengths.max()).long()  # 创建一个全零的张量
    for idx, (seq, seq_len) in enumerate(zip(name_sequences, seq_lengths)):  # 用切片的方法，将数值贴过去
        seq_tensor[idx, :seq_len] = torch.LongTensor(seq)

    # sort by length to use pack_padded_sequence
    seq_lengths, perm_idx = seq_lengths.sort(dim=0, descending=True)  # 返回两个值:排序后的序列及其下标
    seq_tensor = seq_tensor[perm_idx]
    countries = countries[perm_idx]

    return create_tensor(seq_tensor), create_tensor(seq_lengths), create_tensor(countries)



print('Prepare data'.center(100, '-'))
# 字符到字母到assic码独热向量到长短相同

class NameDataSet(Dataset):

    def __init__(self, is_train_set=True):
        filename = 'data/names_train.csv.gz' if is_train_set else 'data/name_test.csv.gz'
        with gzip.open(filename=filename, mode='rt') as f:
            reader = csv.reader(f)
            rows = list(reader)
        self.names = [row[0] for row in rows]
        self.len   = len(self.names)
        self.countries = [row[1] for row in rows]
        self.country_list = list(sorted(set(self.countries)))  # 转成集合会去重+
        self.country_dict = self.getCountryDict()
        self.country_num = len(self.country_list)

    def __getitem__(self, item):  # item==index
        return self.names[item], self.country_dict[self.countries[item]]

    def __len__(self):
        return self.len

    def getCountryDict(self):
        count_dict = dict()
        for idx, country_name in enumerate(self.country_list):
            country_dict[country_name] = idx
        return count_dict

    def idx2country(self, index):
        return self.country_list[index]

    def getCountriesNum(self):
        return self.country_num

hidden_size = 100
batch_size = 256
n_layer = 2
n_epochs = 100
n_chars = 128
use_GPU = False

trainset = NameDataSet(is_train_set=True)
trainloader = DataLoader(trainset, batch_size=batch_size, shuffle=True)
testset = NameDataSet(is_train_set=False)
testloader = DataLoader(testset, batch_size=batch_size, shuffle=False)

n_country = trainset.getCountriesNum()  # 模型最红输出的大小

print('Model Design'.center(100, '-'))
class RNNClassifier(torch.nn.Module):
    def __init__(self, input_size, hidden_size, output_size, n_layer=1, bidirectional=True):
        super(RNNClassifier, self).__init__()
        self.hidden_size = hidden_size
        self.n_layers = n_layer
        self.n_directions = 2 if bidirectional else 1

        self.embedding = torch.nn.Embedding(input_size, hidden_size)  #
        self.gru = torch.nn.GRU(hidden_size,   # 输入是hidden_size
                                hidden_size,   # 输出是hidden_size
                                n_layer,
                                bidirectional=bidirectional)  # 单项还是双向
        """什么是双向神经网络:按照序列的正方向和反方向分别计算隐层, 并将他们拼接
        最终输出output,hidden;hidden = [h1,h2],h1,h2分别为严旭烈正向和反向计算出的结果
        """
        self.fc  = torch.nn.Linear(hidden_size * self.n_directions, output_size)

    def _init_hidden(self, batch_size):
        hidden = torch.zeros(self.n_layers * self.n_directions, batch_size, self.hidden_size)
        return create_tensor(hidden)  # ???

    def forward(self, input, seq_lengths):
        # input shape: B x S -> S x B
        input = input.t()  # 矩阵转置
        batch_size = input.size(1)

        hidden = self._init_hidden(batch_size)
        embedding = self.embedding(input)

        # pick them up
        gru_input = pack_padded_sequence(embedding, seq_lengths)  # 加速计算,将序列长度中的padding去掉

        output, hidden = self.gru(gru_input, hidden)  # hidden是我们需要的
        if self.n_directions == 2:
            hidden_cat = torch.cat([hidden[-1], hidden[-2]], dim=1)
        else:
            hidden_cat = hidden[-1]
        fc_output = self.fc(hidden_cat)  # 维度变换
        return fc_output


print('TrainModel'.center(100, '-'))
def trainModel():
    total_loss = 0
    for i, (names, countries) in enumerate(trainset, 1):
        inputs, seq_lengths, target = make_tensor(names, countries)
        output = classifier(inputs, seq_lengths)
        loss = criterion(output, target)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()
        if i % 10 == 0:
            print(f'[{time_since(start)}] Epoch {epoch}', end='')
            print(f'[{i * len(inputs)} / {len(trainset)}]', end='')
            print(f'loss = {total_loss / (i * len(inputs))}')
            return total_loss

def testModel():
    correct = 0
    total = len(testset)
    print('evaluating trained model ...')
    with torch.no_grad():  # 不计算梯度
        for i, (names, countries) in enumerate(testloader,1):
            inputs, seq_lengths, targets = make_tensor(names, countries)
            output = classifier(inputs, seq_lengths)
            pred   = output.max(dim=1, keepdim=True)[1]
            correct += pred.eq(targets.view_as(pred)).sum().item()

        percent = '%.2f' %(100 * correct / total)
        print(f'Test set: Accuracy {correct} / {total} {percent}%')
    return correct / total


print('Main cycle'.center(100,'-'))

if __name__ == '__main__':
    classifier = RNNClassifier(n_chrs, hidden_size, n_country, n_layer)
    if use_GPU:  # 判断是否使用GPU
        device = torch.device('cuda:0')
        classifier.to(device)

    criterion = torch.nn.CrossEntropyLoss()  # 分类问题常用交叉熵
    optimizer = torch.optim.Adam(classifier.parameters(), lr=.001)

    start = time.time()
    print('Training for %d epochs ...' % n_epochs)
    acc_list = []
    for epoch in range(1, n_epochs + 1):
        # Training cycle
        trainModel()
        acc = testModel()
        acc_list.append(acc)

epoch = np.array(1, len(acc_list) + 1, 1)
acc_list = np.array(acc_list)
plot.plot(epoch, acc_list)
plot.xlabel('Epoch')
plot.ylabel('Accuracy')
plt.grid()
plt.show()


# https://www.kaggle.com/c/sentiment-analysis-on-movie-reviews/data