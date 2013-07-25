#!/usr/bin/python3.2
# -*- coding: utf-8 -*-

import bs4
from bs4 import BeautifulSoup
import re
from subprocess import Popen, PIPE

class Names_calculator:
    def __init__(self, text):
        self.text = text
        self.text_len = len(text)
        self.probable_names = []        
        self.up_letter_words = []
        self.up_letter_words_pos = []
        self.names_lemmas = dict()
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
            if self._is_filtered(str(item.group(1))) and len(str(item.group(3))) > 2:
                self.probable_names.append(item.group(3))
             
    def __calc_names_lemmas(self):
        mystem_out = self._mystem_process(' '.join(self.probable_names), ['-n', '-e utf-8'])
        mystem_lemmas = [item[1] for item in re.findall('(\w+)\{([\w|?]+)\}', mystem_out)]
        l_index = 0
        for name in self.probable_names:
            j = len(name.split()) + len(name.split('-')) - 1
            new_lemma = ' '.join(mystem_lemmas[l_index : l_index + j])
            self.names_lemmas[new_lemma] = Hero_character()
            l_index += j

    def __calc_hero_characters(self):
        mystem_out = self._mystem_process(' '.join(self.up_letter_words), ['-n', '-e utf-8'])
        mystem_lemmas = [item[1] for item in re.findall('(\w+)\{([\w|?]+)\}', mystem_out)]
        l_index = 0
        for i in range(len(self.up_letter_words)):
            word = self.up_letter_words[i]
            pos = self.up_letter_words_pos[i]
            j = len(word.split()) + len(word.split('-')) - 1
            lemma = ' '.join(mystem_lemmas[l_index : l_index + j])
            if lemma in self.names_lemmas.keys():
                hc = self.names_lemmas[lemma]
                hc.count += 1
                hc.positions.append(pos)
                if hc.start < 0:
                    hc.start = pos
                if pos > hc.finish:
                    hc.finish = pos
                hc.name = lemma
            l_index += j

    def _mystem_process(self, raw_content, options):
        with Popen(["./mystem"] + options, stdout=PIPE, stdin=PIPE) as pipe:
            (stdout, stderr) = pipe.communicate(bytes(raw_content, "utf-8"))
            return stdout.decode('utf-8')

    def _is_filtered(self, name_part):
        return name_part == '' or \
               name_part[0] != '«' and \
               name_part[0] != '»' and \
               name_part[0] != ':' and \
               name_part[0] != '.' and \
               name_part[0] != '?' and \
               name_part[0] != '!' and \
               name_part[0] != '[' and \
               name_part[0] != ']' and \
               name_part[0] != '-' and \
               name_part[0] != '—' and \
               name_part[0] != '–' and \
               name_part[0] != '(' and \
               name_part[0] != ')' and \
               name_part[0] != '…' and \
               name_part[0] != '\"'

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
        strings = []
        for ch in item.children:
            if type(ch) == bs4.element.NavigableString:
                strings.append(str(ch))
        return " ".join(strings)

def main():
    f = open("corpus/3_mushkerera.fb2", "rb")
    text = f.read()
    f.close()
    parser = FB2_parser(text)
    nc = Names_calculator(parser.get_text())
    f = open("tmp.txt", "wb");
    for n in nc.get_names():
        f.write(bytes(n.name.encode('utf-8')))
        f.write(bytes('\n'.encode('utf-8')))
    f.close()

if __name__ == "__main__":
    main()
