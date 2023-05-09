from properties import *
from transformers import AutoModel, BertTokenizerFast

import torch


class BertWrapper:
    def __init__(self, device) -> None:
        self.__device = device
        self.__tokenizer = BertTokenizerFast.from_pretrained(properties.bert.version)
        self.__bert = AutoModel.from_pretrained(properties.bert.version).to(device)
        self.__bert.eval()
        for param in self.__bert.parameters():
            param.requires_grad = False

    def __call__(self, text, max_padding: bool = False):
        sent_ids, mask = self.__sentToIds(text, max_padding)
        return self.__bert(sent_ids, mask)

    def __sentToIds(self, texts, max_padding: bool):
        args = {
            'batch_text_or_text_pairs': texts,
            'truncation': True,
            'return_token_type_ids': False
        }
        if max_padding:
            args['max_length'] = properties.bert.token_max_seq_len
            args['padding'] = 'max_length'
        tokens = self.__tokenizer.batch_encode_plus(**args)

        return torch.tensor(tokens['input_ids']).to(self.__device), torch.tensor(tokens['attention_mask']).to(self.__device)



# debaging 