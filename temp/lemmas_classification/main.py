#!/usr/bin/python3

from bs4 import BeautifulSoup as BS
import sys
from subprocess import Popen, PIPE
import re

def main(argv):
    filename = argv[1]
    content = get_p(file_content(filename))
    lemmas = work_with_ps((content, filename, "unknown"))

    raw_metrics = open('result').read().split('\n')[:-1]
    parsed = []

    for line in raw_metrics:
        splitted = line.split(';')
        word_and_counts = splitted[2].split(',')
        
        inner_lemmas = []
        inner_lemmas_count = {}

        for word_and_count in word_and_counts:
            splitted_word_and_count = word_and_count.split('=')
            word = splitted_word_and_count[0]
            count = splitted_word_and_count[1]
            inner_lemmas.append(word)
            inner_lemmas_count[word] = count

        splitted[2] = (set(inner_lemmas), inner_lemmas_count)
        parsed.append(splitted) 

    word_and_count = lemmas.split(';')
    inner_lemmas = []
    inner_lemmas_count = {}
    for word_and_count in word_and_counts:
        splitted_word_and_count = word_and_count.split('=')
        word = splitted_word_and_count[0]
        count = splitted_word_and_count[1]
        inner_lemmas.append(word)
        inner_lemmas_count[word] = count

    orig_set = (set(inner_lemmas), inner_lemmas_count)
    rank = {}

    for ranked_book in list(sorted([(get_metric(orig_set, book[2]), book[1]) for book in parsed]))[:100]:
        rank_genre = ranked_book[1]
        if rank_genre in rank:
            rank[rank_genre] += 1
        else:
            rank[rank_genre] = 1

    
    for genre in list(reversed(sorted(rank, key=lambda x: rank[x])))[:3]:
        print("%s %d" % (genre,rank[genre]))

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

def mystem_process(raw_content):
    with Popen(["./mystem", "-n", "-e utf-8"], stdout=PIPE, stdin=PIPE) as pipe:
        (stdout, stderr) = pipe.communicate(bytes(raw_content, "utf-8"))
        return stdout.decode('utf-8')

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
    for lemma in lemmas_counts[index_from:-index_from]:
        lemmas_string.append("%s=%d" % (lemma[1], lemma[0]))

    log_string = [ 
        name,
        genre,
        ','.join(list(lemmas_string))
    ]
    return ";".join(map(str, log_string))

def get_metric(first_lemmas, second_lemmas):
    first_set = first_lemmas[0]
    second_set = second_lemmas[0]

    min_length = min(len(first_set), len(second_set))	
    intersection = first_set.intersection(second_set)

    weights = []

    for word in intersection:
        weights.append( int(first_lemmas[1][word]) * int(second_lemmas[1][word]) )

    min_weight = min(weights)
    weights = [ (1/(float(weight)/float(min_weight))) for weight in weights]

    # rank = float(len(intersection)) / float(min_length)
    rank = float(sum(weights)) / float(min_length)
    return 1 / rank

if __name__ == "__main__":
    main(sys.argv)
