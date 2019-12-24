#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @package prelm
# @copyright Copyright (c) 2019, Ming-Fan Li.
# @license MIT

""" A Package of Pretained Language Models.
"""

from __future__ import with_statement, absolute_import


__author__ = 'Ming-Fan Li <li_m_f@163.com>'
__version__ = '0.0.2'



#
def get_assignment_map_from_ckpt(init_ckpt,
                                 name_replace_dict={},
                                 trainable_vars=None):
    """ name_replace_dict = { old_name_str_chunk: new_name_str_chunk }
    """
    if trainable_vars is None:
        trainable_vars = tf.trainable_variables()
    #
    name_to_variable = collections.OrderedDict()
    for var in trainable_vars:
        name = var.name
        m = re.match("^(.*):\\d+$", name)
        if m is not None:
            name = m.group(1)
        name_to_variable[name] = var
        #
    
    #
    ckpt_vars = tf.train.list_variables(init_ckpt)
    # 
    assignment_map = collections.OrderedDict()
    for x in ckpt_vars:
        (name, var) = (x[0], x[1])
        #
        for k, v in name_replace_dict.items():
            if k in name:
                name_new = name.replace(k, v)
                break
        else:
            continue
        #
        if name_new not in name_to_variable:
            continue
        #
        assignment_map[name] = name_new
        print("name_old: %s" % name)
        print("name_new: %s" % name_new)
        #
    
    return assignment_map

def remove_from_trainable_variables(non_trainable_names,
                                    trainable_vars=None,
                                    graph=None):
    """
    """
    if graph is None:
        graph = tf.get_default_graph()
    #
    if trainable_vars is None:
        trainable_vars = graph.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
        # tf.trainable_variables()
        
    #    
    graph.clear_collection(tf.GraphKeys.TRAINABLE_VARIABLES)
    #
    for var in trainable_vars:
        for item in non_trainable_names:
            if item in var.name:
                print("not_training: %s" % var.name)
                break
        else:
            graph.add_to_collection(tf.GraphKeys.TRAINABLE_VARIABLES, var)
        #
    #
        
def initialize_with_pretrained_ckpt(init_ckpt,                                    
                                    name_replace_dict={},
                                    non_trainable_names=[],                                    
                                    assignment_map=None,
                                    trainable_vars=None,
                                    graph=None):
    """ name_replace_dict = { old_name_str_chunk: new_name_str_chunk }
        non_trainable_names = ["bert", "word_embeddings"]  # for example
    """
    if assignment_map is None:
        assignment_map = get_assignment_map_from_ckpt(init_ckpt,
                                                      name_replace_dict,
                                                      trainable_vars)
    #
    # assign
    tf.train.init_from_checkpoint(init_ckpt, assignment_map)
    #
    # tune or not
    remove_from_trainable_variables(non_trainable_names, trainable_vars, graph)
    #

