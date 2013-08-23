#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

from visualiser2 import parse_args
import names_grep as ng

class Chain_link():
    def __init__(self, name, position):
        self.name = name
        self.position = position

def main():
    file_name = parse_args()
    fb2 = open(file_name, 'rb').read().decode('utf-8')
    parser = ng.FB2_parser(fb2)
    text = parser.get_text()
    names_greper = ng.Names_calculator(text)
    heroes = names_greper.get_names()
    chain_links = [(hero.name, pos) for hero in heroes for pos in hero.positions]
    chain_links.sort(key=lambda x: x[1])
    print(chain_links[:40])
      

if __name__ == '__main__':
    main()        
