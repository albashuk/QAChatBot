import math

from BertWrapper import BertWrapper
from Dictionary import Dictionary

import string
import torch

from MessageInterpretation import MessageInterpretation
from parser import parseOnWords


class MessageInterpretationService:
    def __init__(self, device, bert: BertWrapper) -> None:
        self.__cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        
        self.__device = device
        self.__bert = bert

    def similarity(self,
                   interp1: MessageInterpretation,
                   interp2: MessageInterpretation,
                   bert_multiplier: float) -> float:
        bert_cos = self.__bertCosSim(interp1.bert_vec, interp2.bert_vec)
        if interp1.dict_vec is None and interp2.dict_vec is None:
            return bert_cos
        else:
            dict_cos = self.__dictCosSim(interp1.dict_vec, interp2.dict_vec)
            return (bert_multiplier * bert_cos + (1 - bert_multiplier) * dict_cos).item()

    def toInterpretation(self, message: str, dictionary: Dictionary) -> MessageInterpretation:
        bert_vec = self.__bert([message])[1]
        dict_vec = self.__dictionaryUse(message, dictionary)

        return MessageInterpretation(bert_vec, dict_vec, dictionary.getVersion())
        
    def __dictionaryUse(self, msg: str, dictionary: Dictionary):
        words = self.__parseMsgOnWords(msg)
        if dictionary.size() == 0:
            dict_vec = None
        else:
            dict_vec = []
            for word in words:
                index = dictionary.index(word)
                if index is not None:
                    dict_vec.append(index)
        return dict_vec

    def __bertCosSim(self, vec1, vec2):
        return self.__cos(vec1, vec2)

    def __dictCosSim(self, dict1, dict2):
        if len(dict1) == 0 or len(dict2) == 0:
            return 0.5 if len(dict1) == 0 and len(dict2) == 0 else 0.0
        return len(set(dict1).intersection(dict2)) / math.sqrt(len(dict) * len(dict2))

    @staticmethod
    def __parseMsgOnWords(msg: str):
        return set(parseOnWords(msg))




# debugging

# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# bert = BertWrapper(device)
# dictionary = Dictionary(None)
# dictionary.set({"London", "Britain"})
# messageSimilarity = MessageSimilarity(device, bert, dictionary, 0.5, 0.7)
# msg1 = "London is the capital of Great Britain"
# msg2 = "Britain comprises England, Scotland, Wales and Northern Ireland."
# print(messageSimilarity(msg1, msg2))
