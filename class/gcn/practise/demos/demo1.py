# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/23 20:44
# FileName: demo1
# Description:
from abc import ABC

import torch
from torch_geometric.data import Data


edge_index = torch.tensor([[0,1,1,2],
                          [1,0,2,1]])  # 定义的是源节点与目标节点的张量,0-1，1-0，1-2，2-1这样连接

x = torch.tensor([[-1], [0], [1]], dtype=torch.float)  # 节点特征
data = Data(x = x, edge_index=edge_index)  # 传入参数将Data类实例化

print('Mini-batches'.center(100, '-'))
# 将所有的mini-batches组成一个稀疏的斜对角矩阵
print('Creating Message Passing Networks'.center(100, '-'))
# 将卷积算子推广到不规则域通常表示为邻域聚合或消息传递方案
# MessagePassing通过自动处理消息来帮助创建传递图神经网络;
# 用户只需要定义函数：message() & update()以及要使用的聚合方案:aggr='add',aggr='mean', aggr='max'

print('Implementing the GCN Layer'.center(100, '-'))
from torch_geometric.nn import MessagePassing
from torch_geometric.utils import add_self_loops, degree

"""
1、创建自联结矩阵
2、线型转换特征矩阵
3、计算归一化系数
4、归一化节点特征
5、将邻居信息聚合
"""

edge_index = torch.tensor([[1,2,3],[0,0,0]], dtype=torch.long) # shape:(2, 3)=(维度, 边的个数)
x = torch.tensor([[1],[1],[1],[1]], dtype=torch.float)  # 节点特征; shape(4,1)=(节点个数,节点个数/in_channels)

print('low-level implementation'.center(100, '-'))
class GCNConv(MessagePassing, ABC):
    def __init__(self, in_channels, out_channels):
        super(GCNConv, self).__init__()  # aggr='add' 默认
        self.linear = torch.nn.Linear(in_features=in_channels,
                                      out_features=out_channels)

    def forward(self, x, edge_index):

        # Step1:Add self-loops to tha adjacency matrix
        edge_index, _ = add_self_loops(edge_index=edge_index, num_nodes=x.size(0))
        # print('Add self-loops edge_index'.center(50,'-'))
        # print(edge_index)

        # Step2: 线型转换特征矩阵
        x = self.linear(x)
        # print('Linear tranform'.center(50, '-'))
        # print(x)

        # Step3：计算归一化
        row, col = edge_index
        # print('\nrow-------', row)
        # print('\ncol-------', col)
        deg = degree(col, x.size(0), dtype=x.dtype)
        # print('degree'.center(50, '-'))
        # print(deg)
        deg_inv_sqrt = deg.pow(-.5)  # 求出度矩阵的逆矩阵
        deg_inv_sqrt[deg_inv_sqrt == float('inf')] = 0  #
        norm = deg_inv_sqrt[row] * deg_inv_sqrt[col]
        # print('norm'.center(50, '-'))
        # print(norm)

        # Step5: Start propagating messages
        return self.propagate(edge_index, x=x, norm=norm)

    def message(self, x_j, norm):

        # print('x_j'.center(50, '-'))
        # print(x_j)
        # print(norm.view(-1, 1) * x_j)

        return norm.view(-1, 1) * x_j

conv = GCNConv(1, 2)
ret = conv(x, edge_index)


print('Example'.center(100, '-'))
import torch
import torch.nn.functional as tf
from torch_geometric.nn import GCNConv


class GNN(torch.nn.Module):
    def __init__(self):
        super(GNN, self).__init__()
        self.conv1 = GCNConv(dataset.num_nodes_features, 16)
        self.conv2 = GCNConv(16, data.num_classes)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index

        x = tf.relu(self.conv1(x))
        x = tf.dropout(x, training=self.training)  # 丢弃部分神经元
        x = self.conv2(x, edge_index)  # 最后一层不激活,直接交给softMax

        return tf.log_softmax(x, dim=1)


model = GNN()

# criterion = tf.nll_loss(size_average=False)
optimizer = torch.optim.Adam(model.parameters(), lr=.01, weight_decay=5e-4)

for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = tf.nll_loss(out[data.tain_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()