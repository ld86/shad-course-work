#!/usr/bin/python3

import sys
from bs4 import BeautifulSoup as BS
import re

def file_content(file):
    # print("Readed %s" % file)
    with open(file, "rb") as f:
        return f.read()

def get_p(content):
    bs = BS(content)
    return [p.text for p in bs.select("body p")]

def get_sentences(file_p):
    sentences = []
    for p in file_p:
        if p.strip() != '':
            sentences.extend(re.split('[.!?]', p));
    return sentences

def is_dialog(sentence):
    return sentence.lstrip().startswith("—") or \
            sentence.lstrip().startswith("–") or \
            sentence.lstrip().startswith("-") 

def get_dialog_positions(sentences):
    dialog_positions = []
    for sentence in zip(sentences, range(len(sentences))):
        if is_dialog(sentence[0]):
            dialog_positions.append(sentence[1])
    return dialog_positions

def main(argv):
    file = argv[1]
    p = get_p(file_content(file))
    sentences = get_sentences(p)
    dialog_positions = get_dialog_positions(sentences)
    print(len(sentences))
    [print(position) for position in dialog_positions]

if __name__ == "__main__":
    main(sys.argv)
