#!/usr/bin/python3.2
#_*_ coding: utf-8 _*_

from visualiser2 import parse_args
import names_grep as ng

def chain():
    file_name = parse_args()
    fb2 = open(file_name, 'rb').read().decode('utf-8')
    parser = ng.FB2_parser(fb2)
    text = parser.get_text()
    names_greper = ng.Names_calculator(text)
    heroes = names_greper.get_names()
    chain_links = [(hero.name, pos) for hero in heroes for pos in hero.positions]
    chain_links.sort(key=lambda x: x[1])
    return chain_links

def find_interact_pairs(chain):
    """здесь происходит формирование множества пар предполагаемого взаимодействия героев.
        pair - это кортеж вида ((hero0_name, hero0_pos), (hero1_name, hero1_pos))"""
    return { (pair[0][0], pair[1][0]) 
            for pair in zip(chain, chain[1:]) 
                if pair[1][1] - pair[0][1] < 100 }

def main():
    hero_chain = chain()
    pairs = find_interact_pairs(hero_chain)
    for pair in pairs:
        print(pair)

if __name__ == '__main__':
    main()        
