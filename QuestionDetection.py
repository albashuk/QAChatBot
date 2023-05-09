from properties import properties
from BertWrapper import BertWrapper

import pathlib 
import datetime
import torch
import torch.nn as nn


class QuestionDetection():
    
    class __Module(nn.Module):

        class __ModuleEnd(nn.Module):
            def __init__(self) -> None:
                super().__init__()

                self.__drop = nn.Dropout(properties.dropout_prob)
                self.__ln = nn.Linear(properties.bert.out_size, 2)
                self.__softmax = nn.Softmax(dim=1)

            def forward(self, x):
                x = self.__drop(x)
                x = self.__ln(x)
                x = self.__softmax(x)

                return x

        #####################################################################

        def __init__(self, bert: BertWrapper, path = None) -> None:
            super().__init__()

            self.__bert = bert
            self.__moduleEnd = self.__ModuleEnd()
            if (path != None):
                self.load(path)

        def forward(self, sentences):
            x = self.__bert(sentences, max_padding=True)[1]
            x = self.__moduleEnd(x)

            return x

        def save(self, path):
            torch.save(self.__moduleEnd.state_dict(), path)

        def load(self, path):
            self.__moduleEnd.load_state_dict(torch.load(path))

    #########################################################################

    def __init__(self, device, bert: BertWrapper, path = None) -> None:
        self.__device = device
        self.__module = self.__Module(bert, path).to(device)

    def isQuestion(self, sentence) -> bool:
        self.__module.eval()
        has_question_mark = 1.0 if "?" in sentence else 0.0
        question_prob = self.__module([sentence])[0]
        return question_prob[0].item() <= question_prob[1].item() + has_question_mark * properties.question_mark_weight

    def train(self, train_dataset, valid_dataset, train_batch_size, valid_batch_size, criterion, learning_rate, epochs):
        self.__module.train()

        train_loader = torch.utils.data.DataLoader(dataset=train_dataset, batch_size=train_batch_size)
        valid_loader = torch.utils.data.DataLoader(dataset=valid_dataset, batch_size=valid_batch_size)
        optimizer = torch.optim.Adam(self.__module.parameters(), lr = learning_rate)

        correctness_rate = []
        for epoch in range(epochs):
            for x, y in train_loader:
                optimizer.zero_grad()

                _y = torch.zeros(len(y), 2).to(self.__device)
                for i in range(len(y)):
                    _y[i][y[i]] = 1

                yhat = self.__module(x)
                loss = criterion(_y, yhat)
                loss.backward()
                optimizer.step()
            print("Trained: ", 100 * (epoch + 1) / epochs, "%", end="\r")

            correct = 0
            for x, y in valid_loader:
                _, yhat = torch.max(self.__module(x), 1)
                yhat.to(self.__device)
                y = torch.tensor(y).to(self.__device)
                correct += (y == yhat).sum().item()
            correctness_rate.append(100 * (correct / len(valid_dataset)))
            print("Validated: ", 100 * (epoch + 1) / epochs, "%", end="\r")

        self.__module.eval()
        self.saveModuleToFile()
        return correctness_rate

    def saveModuleToFile(self, path = "default", filename = "default"):
        save_to_last_version = (path == "default" and  filename == "default")

        if (path == "default"):
            path = "modules/QuestionDetection/versions/"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        if (filename == "default"):
            dt = datetime.datetime.now()
            filename = dt.strftime("%y-%m-%d-%H-%M-%S") + ".pt"

        self.__module.save(path + filename)
        if (save_to_last_version):
            self.__module.save("modules/QuestionDetection/last.pt")

    def loadModuleFromFile(self, path = "default"):
        if (path == "default"):
            path = "modules/QuestionDetection/last.pt"
        self.__module.load(path)


# debugging

# q = QuestionDetection()
# q.saveModuleToFile()
# q.loadModuleFromFile()
# q.loadModuleFromFile("modules/QuestionDetection/versions/23-02-26-13-22-39.pt", short = True)
# q.isQuestion(["A B C D ?"])
# print(torch.cuda.is_available())

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# bert = BertWrapper(device)
# QD = QuestionDetection(device, bert)
#
# from QuestionDetDataset import QuestionDetDataset
# train_dataset, valid_dataset = QuestionDetDataset.getDataset("SQuAD")
# correctness_rate = QD.train(train_dataset, valid_dataset, 100, 5000, nn.CrossEntropyLoss(), properties.learning_rate, properties.epochs)
#
# import numpy as np
# num = len(correctness_rate)
# x = np.arange(1,num+1)
# y = np.array(correctness_rate)
#
# import matplotlib.pyplot as plt
# plt.plot(x, y)
# plt.show()
