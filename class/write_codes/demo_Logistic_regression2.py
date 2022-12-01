# coding: utf-8
# Author: ryrl
# CreateTime: 2022/5/9 19:48
# FileName: demo_Logistic_regression2
# Description:

import torch
import torchvision
import torch.nn.functional as tf

train = torchvision.datasets.MNIST('../../data/',
                                   train=True,
                                   download=True)
test = torchvision.datasets.MNIST('../../data/',
                                  train=False,
                                  download=True)

