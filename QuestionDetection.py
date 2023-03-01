from properties import *
import pathlib 
import datetime
import torch
import torch.nn as nn
from transformers import AutoModel, BertTokenizerFast


class QuestionDetection():
    
    class __Module(nn.Module):

        class __ModuleEnd(nn.Module):
            def __init__(self) -> None:
                super().__init__()

                self.__drop = nn.Dropout(properties.dropout_porb)
                self.__ln = nn.Linear(properties.bert.out_size,2)
                self.__softmax = nn.Softmax()

            def forward(self, x):
                x = self.__drop(x)
                x = torch.tanh(self.__ln(x))
                x = self.__softmax(x)

                return x

        #####################################################################

        def __init__(self, path = None, short = False) -> None:
            super().__init__()

            if (path == None or short == True):
                self.__downloadBert()
            self.__moduleEnd = self.__ModuleEnd()
            if (path != None):
                self.load(path, short)

        def forward(self, sent_ids, mask):
            x = self.__bert(input_ids=sent_ids, attention_mask=mask)[1]
            x = self.__moduleEnd(x)

            return x

        def train(self):
            super().train()
            self.__bert.eval()

        def save(self, path, short = True):
            if short:
                torch.save(self.__moduleEnd.state_dict(), path)
            else:    
                torch.save(self.state_dict(), path)

        def load(self, path, short = True):
            if short:
                self.__moduleEnd.load_state_dict(torch.load(path))
            else:
                self.load_state_dict(torch.load(path))

        def __downloadBert(self):
            self.__bert = AutoModel.from_pretrained(properties.bert.version)
            for param in self.__bert.parameters():
                param.requires_grad = False

    #########################################################################

    def __init__(self, path = None, short = False) -> None:
        self.__module = self.__Module(path, short)
        self.__max_seq_len = properties.bert.token_max_seq_len
        self.__tokenizer = BertTokenizerFast.from_pretrained(properties.bert.version)

    def isQuestion(self, sentence):
        self.__module.eval()

        sent_ids, mask = self.__sentToIds(sentence)
        preds = self.__module.forward(sent_ids, mask)

        return preds

    def train(self, train_dataset, valid_dataset, train_batch_size, valid_batch_size, criterion, learning_rate, epochs):
        self.__module.train()

        train_loader = torch.utils.data.DataLoader(dataset = train_dataset, batch_size = train_batch_size)
        valid_loader = torch.utils.data.DataLoader(dataset = valid_dataset, batch_size = valid_batch_size)
        optimizer = torch.optim.ADAM(self.__module.parameters(), lr = learning_rate)

        correctness_rate = []
        for epoch in range(epochs):
            for x, y in train_loader:
                optimizer.zero_grad()
                _y = torch.zeros(2)
                _y[y] = 1
                yhat = self.__module(self.__sentToIds(x))
                loss = criterion(_y, yhat)
                loss.backward()
                optimizer.step()

            correct = 0
            for x, y in valid_loader:
                yhat = torch.max(self.__module(self.__sentToIds(x)), 1)
                correct += (y == yhat).sum().item()
            correctness_rate.append(100 * (correct / len(valid_dataset)))

        self.__module.eval()
        self.saveModuleToFile()
        return correctness_rate

    def saveModuleToFile(self, path = "default", filename = "default", short = True):
        save_to_last_version = (path == "default" and  filename == "default")

        if (path == "default"):
            path = "modules/QuestionDetection/versions/"
        pathlib.Path(path).mkdir(parents=True, exist_ok=True)

        if (filename == "default"):
            dt = datetime.datetime.now()
            filename = dt.strftime("%y-%m-%d-%H-%M-%S") + ".pt"

        self.__module.save(path + filename, short)
        if (save_to_last_version):
            self.__module.save("modules/QuestionDetection/last.pt", short = False)

    def loadModuleFromFile(self, path = "default", short = False):
        if (path == "default"):
            path = "modules/QuestionDetection/last.pt"
            short = False
        self.__module.load(path, short)

    def __sentToIds(self, sentences):
        tokens = self.__tokenizer.batch_encode_plus(
            sentences,
            max_length = self.__max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False 
        )

        return torch.tensor(tokens['input_ids']), torch.tensor(tokens['attention_mask'])


# debuging

# q = QuestionDetection()
# q.saveModuleToFile()
# q.loadModuleFromFile()
# q.loadModuleFromFile("modules/QuestionDetection/versions/23-02-26-13-22-39.pt", short = True)
# q.isQuestion(["A B C D ?"])

# trainin