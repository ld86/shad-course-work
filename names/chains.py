#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

from visualiser2 import parse_args
import names_grep as ng

class Chain_link():
    def __init__(self, name, position):
        self.name = name
        self.position = position
        self.dist = 0
        self.the_next = None
        
