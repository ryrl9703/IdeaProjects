# coding: utf-8
# Author: ryrl
# CreateTime: 2022/4/25 16:07
# FileName: demo_SimGNN
# Description:

import torch
import torch_geometric
from utils import tab_printer
from simgnn import SimGNNTrainer

# edge_index = torch.tensor([[0, 1, 1, 2],  # 源节点
#                            [1, 0, 2, 1]],   # 目标节点
#                           dtype=torch.long)
#
# x = torch.tensor([[-1], [0], [1]], dtype=torch.float)

