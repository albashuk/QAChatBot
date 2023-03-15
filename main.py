from properties import *
from QuestionDetDataset import *
from QuestionDetection import *

import torch.nn as nn
import matplotlib.pyplot as plt
import numpy as np

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
QD = QuestionDetection(device)

train_dataset, valid_dataset = QuestionDetDataset.getDataset("SQuAD")
correctness_rate = QD.train(train_dataset, valid_dataset, 100, 5000, nn.CrossEntropyLoss(), properties.learning_rate, properties.epochs)

num = len(correctness_rate)
x = np.arange(1,num+1)
y = np.array(correctness_rate)

plt.plot(x, y)
plt.show()