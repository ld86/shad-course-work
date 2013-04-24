#!/usr/bin/python3
# -*- coding: utf-8 -*-

import pickle
import sys
import itertools
from bs4 import BeautifulSoup as BS
from glob import glob
from subprocess import Popen, PIPE
from multiprocessing import Pool
import re
import math

genres = \
    [
        "det_action",
        "child_prose",
        "love_history",
        "religion_rel",
        "sf",
        "detective",
        "thriller",
        "children",
        "child_sf",
        "love_contemporary",
        "prose_history",
        "prose_rus_classic",
        "prose_su_classics",
        "prose_contemporary",
        "sf_history",
        "sf_action",
        "sf_fantasy",
        "humor_prose"
    ]


def main(): 
    with open("result", "w") as log:
        log.flush()
        with open("more_result", "w") as more:
            for genre in genres:
                process_genre(genre, log, more)

def work_with_ps(genre_p_and_name_and_genre):
    genre_p, name, genre = genre_p_and_name_and_genre
    print("Process %s" % name)
    words = mystem_process(" ".join(genre_p)).split("\n")
    
    lemmas = {}

    for word in words:
        orig, lemma = parse_word(word)
        if lemma in lemmas:
            lemmas[lemma] += 1
        else:
            lemmas[lemma] = 1

    lemmas_counts = []
    for lemma in lemmas:
        lemmas_counts.append((lemmas[lemma], lemma))

    lemmas_counts = sorted(lemmas_counts, reverse=True)
    lemmas_counts_length = len(lemmas_counts)
    index_from = int(lemmas_counts_length/3)
    lemmas_string = []
    print(lemmas_counts[0:5])
    for lemma in lemmas_counts[index_from:-index_from]:
        lemmas_string.append("%s=%d" % (lemma[1], lemma[0]))

    log_string = [ 
        name,
        genre,
        ','.join(list(lemmas_string))
    ]
    return ";".join(map(str, log_string))

def process_genre(genre, log, more):
    print("Process %s" % genre)
    genre_path = "../corpus/flibusta/%s/*.fb2" % genre
    genre_files = get_files(genre_path)
    
    pool = Pool(10)
    genre_ps = pool.map(lambda file: get_p(file_content(file)), genre_files)
    pool.close()
    pool.join()

    pool = Pool(10)
    metrics = pool.map(work_with_ps, zip(genre_ps, genre_files, itertools.repeat(genre)))
    pool.close()
    pool.join()    
    #metrics = map(work_with_ps, zip(genre_ps, genre_files, itertools.repeat(genre)))
    for metric in metrics:
        print(metric, file=log)
    log.flush()

    # total_sentences_count
    # total_sentences_long
    # total_book_len
    # total_dialogs_count
    # total_words_len
    # total_words_count
    # lemmas
    # punctuation


def count_metrics(genre_p):
    sentences_long = 0
    sentences_count = 0
    book_len = 0
    dialogs_count = 0
    words_len = 0
    words_count = 0
    lemmas = set()
    punctuation = 0

    for p in genre_p:
        # Sentences work
        sentences = [sentence for sentence in p.split(".") if sentence != '']
        sentences_count += len(sentences)
        for sentence in sentences:
            sentences_long += len(sentence)

            # Dialogs count
            if  sentence.lstrip().startswith("—") is True or \
                sentence.lstrip().startswith("–") is True or \
                sentence.lstrip().startswith("-") is True:
                dialogs_count += 1

        # Book len
        book_len += len(p)

        # Punctuation
        for i in ",.!?;:-":
            punctuation += p.count(i)
    
    words = mystem_process(" ".join(genre_p)).split("\n")
    words_count = len(words)
    for word in words:
        orig, lemma = parse_word(word)
        words_len += len(orig)
        lemmas.add(lemma)

    return \
        [
            sentences_long, 
            sentences_count, 
            book_len,
            dialogs_count,
            words_len,
            words_count,
            lemmas,
            punctuation
        ]

def mystem_process(raw_content):
    with Popen(["./mystem", "-n", "-e utf-8"], stdout=PIPE, stdin=PIPE) as pipe:
        (stdout, stderr) = pipe.communicate(bytes(raw_content, "utf-8"))
        return stdout.decode('utf-8')

mystem_re = re.compile("(.+){(.+)}")
def parse_word(word):
    matched = mystem_re.match(word)
    if matched is None:
        return [word, ""]
    return (matched.group(1), matched.group(2))

def get_p(content):
    bs = BS(content)
    return [p.text for p in bs.select("body p")]

def file_content(file):
    print("Readed %s" % file)
    with open(file, "rb") as f:
        return f.read()

def get_files(path):
    return [file for file in glob(path)]

if __name__ == "__main__":
    main()
    #compare(sys.argv[1])
    

    #for genre in genres:
    #    genre_path = "flibusta/%s/*.fb2" % genre
    #    genre_files = get_files(genre_path)
    #    for file in genre_files:
    #        print(file)
    #        compare(file)
