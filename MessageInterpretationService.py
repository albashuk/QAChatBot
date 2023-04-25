from BERT import BERT
from Dictionary import Dictionary

import string
import torch

from MessageInterpretation import MessageInterpretation


class MessageInterpretationService:
    def __init__(self, device, bert: BERT) -> None:
        self.__cos = torch.nn.CosineSimilarity(dim=1, eps=1e-6)
        
        self.__device = device
        self.__bert = bert

    def similarity(self,
                   interp1: MessageInterpretation,
                   interp2: MessageInterpretation,
                   bert_multiplier: float) -> float:
        bert_cos = self.__cos(interp1.bert_v, interp2.bert_v)
        dict_cos = self.__cos(interp1.dict_v, interp2.dict_v)

        return (bert_multiplier * bert_cos + (1 - bert_multiplier) * dict_cos).item()

    def toInterpretation(self, message: str, dictionary: Dictionary) -> MessageInterpretation:
        bert_v = self.__bert([message])[1]
        dict_v = self.__dictionaryUse(message, dictionary)

        return MessageInterpretation(bert_v, dict_v)
        
    def __dictionaryUse(self, msg: str, dictionary: Dictionary):
        words = self.__parseMsgOnWords(msg)
        dict_v = [0.0] * dictionary.size()
        for word in words:
            if dictionary.index(word) is not None:
                dict_v[dictionary.index(word)] += 1
        return torch.tensor([dict_v]).to(self.__device)

    @staticmethod
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
