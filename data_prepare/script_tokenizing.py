# -*- coding: utf-8 -*-

import os

from ZhongLP.converter import Converter
from ZhongLP.segmenter import Segmenter
from ZhongLP import utils_zh

from Zeras.data_parallelism import DataParallelism
from Zeras.vocab import Vocab


#
import argparse
def parse_args():
    """
    Parses command line arguments.
    """
    parser = argparse.ArgumentParser('bert_data_raw_seg_task')
    parser.add_argument('--note', type=str, default = 'note_something',
                        help = 'make some useful notes')
    
    parser.add_argument('--dir_vocab', type=str, default = '../vocab',
                        help = 'directory for storing tokens file')
    parser.add_argument('--dir_base', type=str, default = '../bert_corp_seg',
                        help = 'base dir for storing genarated data')
    parser.add_argument('--dir_data', type=str, default = None,
                        help = 'data raw dir')
    parser.add_argument('--data', choices=['train', 'valid', 'test'],
                        default = 'train', help = 'data to be processed')
    
    # process truely parallel, but only working in cmd line mode (not IDE)
    parser.add_argument('--worker_type', choices=['process', 'thread'],
                        default = 'thread', help = 'worker type')  # process
    parser.add_argument('--workers', type=int, default = 2,    # 8
                        help = 'number of workers')
    parser.add_argument('--pack_size', type=int, default = 100,     # 10000
                        help = 'pack size')
    parser.add_argument('--group_size', type=int, default = 10,  # 50000
                        help = 'group size')
    
    return parser.parse_args()


#
def clean_text_line(line):
    """
    """    
    line = line.strip().lower()
    line = utils_zh.convert_quan_to_ban(line)
    line = " ".join(line.split())
    
    return line


class DataPreparation():
    """
    """
    def __init__(self):
        """
        """
        pass


#
if __name__ == '__main__':
    
    args = parse_args()
    #
    data = args.data
    if data == 'train':
        pass
    elif data == 'valid':
        pass
    elif data == 'test':
        pass
    else:
        assert False, 'NOT supported data tag'
    #
    dir_data = args.dir_data
    if dir_data is None:
        dir_data = "../corpus_raw/data_raw_" + data
        #
    #
    print(dir_data)
    #
    # files
    list_files = DataParallelism.get_files_with_ext(dir_data, 'txt', flag_walk=True)
    converter = Converter()
    segmenter = Segmenter()
    #
    list_files.sort(key=lambda x: x)
    num_all = len(list_files)
    print("num_all: %d" % num_all)
    #
    group_size = args.group_size
    num_groups = num_all // group_size
    if num_groups * group_size < num_all: num_groups += 1
    #
    dir_base = args.dir_base
    dir_vocab = args.dir_vocab   
    if not os.path.exists(dir_vocab): os.mkdir(dir_vocab)
    if not os.path.exists(dir_base): os.mkdir(dir_base)
    #

    #
    idx_start = 0
    idx_end = num_groups # num_groups
    #
    for idx in range(idx_start, idx_end):
        
        print("curr: %d / %d" % (idx + 1, num_groups))
        #
        posi_start = idx * group_size
        posi_end = posi_start + group_size
        posi_end = min(posi_end, num_all)
        #
        print("%d, %d" % (posi_start, posi_end))
        #

        #
        args.dir_base = os.path.join(dir_base, "partition_%d" % idx)
        args.dir_vocab = os.path.join(dir_vocab, "partition_%d" % idx)
        if not os.path.exists(args.dir_vocab): os.mkdir(args.dir_vocab)
        if not os.path.exists(args.dir_base): os.mkdir(args.dir_base)        
        #
        list_curr = list_files[posi_start:posi_end]
        #

        #
        data_pp = DataPreparation(list_curr, segmenter, args)
        #
        print('running with args : {}'.format(args))
        print("num_files: %d" % len(list_curr))
        #
        data_pp.do_preparation()
        print("articles segmented")
        #
        if data == 'train':            
            file_path = os.path.join(args.dir_vocab, "vocab_tokens.txt")
            data_pp.vocab.save_tokens_to_file(file_path)
            print('vocab saved')
        #
        print("data_pp task finished")
        #
    #
    print("data_pp processed all files")
    #
    if data == 'train':
        vocab = Vocab()  # (lower=True)
        dir_vocab_temp = os.path.join(dir_vocab, "partition_temp")
        for idx in range(num_groups):
            dir_vocab_curr = dir_vocab_temp.replace("temp", str(idx))
            file_path = os.path.join(dir_vocab_curr, "vocab_tokens.txt")
            vocab.add_tokens_from_file(file_path)
        #
        file_path = os.path.join(dir_vocab, "vocab_tokens.txt")
        vocab.save_tokens_to_file(file_path)
        #
        file_path = os.path.join(dir_vocab, "vocab_tokens_no_count.txt")
        vocab.save_tokens_to_file_no_count(file_path)
        print('vocab merged and saved')
    #
    print("data_pp task finished")    
    #
    
    
