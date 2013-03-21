#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as BS
from glob import glob
from subprocess import Popen, PIPE
from multiprocessing import Pool
import re

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
        with open("more_result", "w") as more:
            for genre in genres:
                process_genre(genre, log, more)


def process_genre(genre, log, more):
    print("Process %s" % genre)
    genre_path = "flibusta/%s/*.fb2" % genre
    genre_files = get_files(genre_path)
    genre_ps = list(map(lambda file: get_p(file_content(file)), genre_files[:10]))

    genre_metrics = []

    for genre_p_and_name in zip(genre_ps, genre_files):
        genre_p, name = genre_p_and_name
        print("Process %s" % name)
        metrics = count_metrics(genre_p)
        genre_metrics.append(metrics)

    # total_sentences_count
    # total_sentences_long
    # total_book_len
    # total_dialogs_count
    # total_words_len
    # total_words_count
    # lemmas
    # punctuation

    total = [0, 0, 0, 0, 0, 0, set(), 0]
    print("Process total metrics")
    for metrics in genre_metrics:
        for i in [0, 1, 2, 3, 4, 5, 7]:
            total[i] += metrics[i]
        total[6] = total[6].union(metrics[6])

    log_string =    [
                        genre,
                        str(total[0] / total[1]),
                        str(total[4] / total[5]),
                        str(total[3] / total[0]),
                        str(total[2] / len(genre_metrics)),
                        str(len(total[6])),
                        str(total[7] / len(genre_metrics))
                    ]

    print(";".join(log_string), file=log)
    print(genre_metrics, file=more)
    log.flush()

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
                sentence.lstrip().startswith("–") is True:
                dialogs_count += 1

        # Book len
        book_len += len(p)

        # Punctuation
        for i in ",.!?;:-":
            punctuation += p.count(i)
    
    words = mystem_process(" ".join(genre_p)).split("\n")
    words_count = len(words)
    print(words[:10])
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

