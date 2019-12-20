# -*- coding: utf-8 -*-

import json
from collections import OrderedDict


from Zeras.vocab import Vocab


vocab_file = "../vocab/vocab_tokens_all.txt"
vocab = Vocab()
vocab.add_tokens_from_file(vocab_file)
print(vocab.size())
dict_count = vocab.dict_token_cnt

#
count_filter = 60
#
vocab.filter_tokens_by_cnt(count_filter)
print(vocab.size())
vocab_filtered = "../vocab/vocab_tokens_filtered_%d.txt" % count_filter
vocab.save_tokens_to_file(vocab_filtered)
#
vocab_no_count = "../vocab/vocab_tokens_no_count.txt"
vocab.save_tokens_to_file_no_count(vocab_no_count)
#
vocab_no_count = "../model_configs_vocab/vocab_tokens_no_count.txt"
vocab.save_tokens_to_file_no_count(vocab_no_count)
#

print(len(dict_count))
od_count = OrderedDict()
print(len(od_count))
od_count.update(dict_count)
print(len(od_count))

od_count = dict(sorted(od_count.items(), key=lambda x: x[1]))

"""
#
idx_s = 999900
idx_e = idx_s + 10
#
for idx in range(idx_s, idx_e): print(od_count[idx])
#
"""

dict_minor = {}
for key in od_count.keys():
    if od_count[key] < count_filter:
        dict_minor[key] = od_count[key]
    #

file_minor = "../vocab/minor_tokens_filtered_%d.txt" % count_filter
with open(file_minor, "w", encoding="utf-8") as fp:
    json.dump(dict_minor, fp, ensure_ascii=False, indent = 2)
        
