from BERT import BERT
from Dictionary import Dictionary

import string
import torch

class MessageSimilarity:
    def __init__(self, device, bert: BERT, dictionary: Dictionary, bert_multiplier, threshold) -> None:
        self.__cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        
        self.__device = device
        self.__bert = bert
        self.__dictionary = dictionary
        self.__bert_multiplier = bert_multiplier
        self.__threshold = threshold

    def __call__(self, msg1: str, msg2: str) -> bool:
        bert1, dict1 = self.__msgToVecs(msg1)
        bert2, dict2 = self.__msgToVecs(msg2)

        bert_cos = self.__cos(bert1, bert2)
        dict_cos = self.__cos(dict1, dict2)

        return (self.__bert_multiplier * bert_cos + (1 - self.__bert_multiplier) * dict_cos).item() >= self.__threshold

    def __msgToVecs(self, msg):
        bert = self.__bert([msg])[1]
        dictionary = self.__dictionaryUse(msg)

        return bert, dictionary
        
        
    def __dictionaryUse(self, msg: str):
        words = MessageSimilarity.__parseMsgOnWords(msg)
        dict = [0.0] * self.__dictionary.size()
        for word in words:
            if self.__dictionary.index(word) != None:
                dict[self.__dictionary.index(word)] += 1
        return torch.tensor([dict]).to(self.__device)


    def __parseMsgOnWords(msg: str):
        return {word.strip(string.punctuation) for word in msg.split()}




# debuging

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# bert = BERT(device)
# dictionary = Dictionary(None)
# dictionary.set({"London", "Britain"})
# messageSimilarity = MessageSimilarity(device, bert, dictionary, 0.5, 0.7)
# msg1 = "London is the capital of Great Britain"
# msg2 = "Britain comprises England, Scotland, Wales and Northern Ireland."
# print(messageSimilarity(msg1, msg2))
