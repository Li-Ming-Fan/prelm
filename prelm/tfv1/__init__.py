# -*- coding: utf-8 -*-



import re
import collections

import tensorflow as tf


#
def get_assignment_map_samename(init_ckpt, list_vars=None):
    """
    """
    if list_vars is None:
        list_vars = tf.global_variables()
    #
    name_to_variable = collections.OrderedDict()
    for var in list_vars:
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
        if name not in name_to_variable:
            continue
        #
        assignment_map[name] = name
        print("assigned_variable name: %s" % name)
        #
    
    return assignment_map

#
def get_assignment_map_replaced(init_ckpt,
                                name_replacement_dict={},
                                list_vars=None):
    """ name_replacement_dict = { old_name_str_chunk: new_name_str_chunk }
    """
    if list_vars is None:
        list_vars = tf.global_variables()
    #
    name_to_variable = collections.OrderedDict()
    for var in list_vars:
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
        for k, v in name_replacement_dict.items():
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

def remove_from_trainable_variables(non_trainable_names, trainable_vars=None):
    """
    """
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
        
def initialize_from_ckpt(init_ckpt,                                    
                         name_replacement_dict={},
                         non_trainable_names=[],
                         list_vars=None,                                  
                         assignment_map=None):
    """ name_replacement_dict = { old_name_str_chunk: new_name_str_chunk }
        non_trainable_names = ["bert", "word_embeddings"]  # for example
    """
    if assignment_map is None:
        assignment_map = get_assignment_map_replaced(init_ckpt,
                                                     name_replacement_dict,
                                                     list_vars)
    #
    # assign
    tf.train.init_from_checkpoint(init_ckpt, assignment_map)
    #
    # tune or not
    remove_from_trainable_variables(non_trainable_names, list_vars)
    #

    
    