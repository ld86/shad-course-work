#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import re
from my_subprocess import IPopen

class Names_calculator:
    def __init__(self, text):
        self.text = text
        self.text_len = len(text)
        self.probable_names = []        
        self.up_letter_words = []
        self.up_letter_words_pos = []
        self.names_lemmas = dict()
        self.lemma_pipe = IPopen(["./mystem",'-ne', 'utf-8'])
        self.lexic_pipe = IPopen(["./mystem", '-ine', 'utf-8'])
        self.__calc_names()
        self.__calc_names_lemmas()
        self.__calc_hero_characters()

    def get_names(self):
        return list(self.names_lemmas.values())

    def __calc_names(self):
        iterator = re.finditer(\
            "([.?!«\"»()\[\]–—–…])?(\s+)([А-Я][а-я]*(?:(?:\s+|-)[А-Я][а-я]*)*)(?=[.?!\s,;:\)\"»])", \
            self.text)
        for item in iterator:
            self.up_letter_words.append(item.group(3)) 
            self.up_letter_words_pos.append(item.start())
            if self._is_filtered(str(item.group(1))):
                self.probable_names.append(item.group(3))
             
    def __calc_names_lemmas(self):
        for name in self.probable_names:
            mystem_lemma = self._mystem_process(name, self.lemma_pipe)
            check_info = self._mystem_process(name, self.lexic_pipe)
            if ('PR' not in check_info and 
                'гео' not in check_info and
                'INT' not in check_info):
                new_lemma = ' '.join([item[1] for item in re.findall('(\w+)\{([\w|?]+)\}', mystem_lemma)])
                self.names_lemmas[new_lemma] = Hero_character()

    def __calc_hero_characters(self):
        for (word, pos) in zip(self.up_letter_words, self.up_letter_words_pos):
            mystem_lemma = self._mystem_process(word, self.lemma_pipe)
            lemma = ' '.join([item[1] for item in re.findall('(\w+)\{([\w|?]+)\}', mystem_lemma)])
            if lemma in self.names_lemmas:
                hc = self.names_lemmas[lemma]
                hc.count += 1
                hc.positions.append(pos)
                if hc.start < 0:
                    hc.start = pos
                if pos > hc.finish:
                    hc.finish = pos
                hc.name = lemma

    def _mystem_process(self, raw_content, pipe):
        return pipe.correspond(raw_content + '\n')

    def _is_filtered(self, name_part):
        return (name_part == '' or 
               name_part[0] != '«' and 
               name_part[0] != '»' and 
               name_part[0] != ':' and 
               name_part[0] != '.' and 
               name_part[0] != '?' and 
               name_part[0] != '!' and 
               name_part[0] != '[' and 
               name_part[0] != ']' and 
               name_part[0] != '-' and 
               name_part[0] != '—' and 
               name_part[0] != '–' and 
               name_part[0] != '(' and 
               name_part[0] != ')' and 
               name_part[0] != '…' and 
               name_part[0] != '"')

class Hero_character:
    def __init__(self):
        self.count = 0
        self.start = -1
        self.finish = -1
        self.name = ''
        self.positions = []

    def sort_key(self):
        return self.count

class FB2_parser:
    def __init__(self, inp_text):
        self.text = inp_text
        self.soup = BeautifulSoup(inp_text)
        self.pure_text = ""

    def get_text(self):
        if self.pure_text == "":
            self.pure_text = '. '.join( \
                [str(self._decompose(item)) for item in self.soup.find('body').find_all('p')])
        return self.pure_text
    
    def _decompose(self, item):
        if item.string:
            return item.string
        strings = [str(ch) for ch in item.children if type(ch) == bs4.element.NavigableString]
        return " ".join(strings)

def main():
    f = open("corpus/vlast_colets.fb2", "rb")
    text = f.read()
    f.close()
    parser = FB2_parser(text)
    nc = Names_calculator(parser.get_text())
    print(list(filter(lambda x: x != '', 
                    [hero.name for hero in 
                    sorted(nc.get_names(), key = lambda x: x.sort_key(), reverse = True)]))
        )
if __name__ == "__main__":
    main()
