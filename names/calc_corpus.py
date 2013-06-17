#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

import visualiser2 as visual
import os
import glob


def corpus_handle(path):
    for fb2 in glob.glob(path + '*.fb2*'):
        visual.run(fb2)

    for fs_obj in os.listdir(path):
        if os.path.isdir(path + fs_obj) == True:
            corpus_handle(path + fs_obj + '/') 


corpus_handle('corpus/') 
