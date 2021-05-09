# -*- coding: utf-8 -*-
import numpy as np
from transformers import BertTokenizer, BertConfig


class Tokenizer:
    def __init__(self):
        config = BertConfig.from_json_file(
            'resources/sentence_ru_cased_L-12_H-768_A-12_pt/bert_config.json'
        )
        self._bert_tokenizer = BertTokenizer.from_pretrained(
            'resources/sentence_ru_cased_L-12_H-768_A-12_pt',
            from_pt=True,
            config=config,
            do_lower_case=True,
        )

    def run(self, sentence_list):
        tokens_dict = self._bert_tokenizer.batch_encode_plus(
            sentence_list,
            add_special_tokens=True,
            max_length=128,
            return_attention_mask=True,
            return_token_type_ids=True,
            pad_to_max_length=True,
            return_tensors="np",
        )
        tokens_array = np.array(
            [
                tokens_dict['input_ids'],
                tokens_dict['token_type_ids'],
                tokens_dict['attention_mask']
            ],
            dtype=np.int
        )
        return tokens_array
