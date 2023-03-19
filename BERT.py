from properties import *
from transformers import AutoModel, BertTokenizerFast

import torch

class BERT:
    def __init__(self, device) -> None:
        self.__device = device
        self.__tokenizer = BertTokenizerFast.from_pretrained(properties.bert.version)
        self.__bert = AutoModel.from_pretrained(properties.bert.version).to(device)
        self.__bert.eval()
        for param in self.__bert.parameters():
            param.requires_grad = False

    def __call__(self, sentences):
        sent_ids, mask = self.__sentToIds(sentences)
        return self.__bert(sent_ids, mask)

    def __sentToIds(self, sentences):
        tokens = self.__tokenizer.batch_encode_plus(
            sentences,
            max_length = properties.bert.token_max_seq_len,
            pad_to_max_length=True,
            truncation=True,
            return_token_type_ids=False 
        )

        return torch.tensor(tokens['input_ids']).to(self.__device), torch.tensor(tokens['attention_mask']).to(self.__device)



# debaging 