#!/usr/bin/python3

import sys

def compare_with_other(what, others):
    print(what[0])
    rank_list = []
    what_set = what[2]
    for other in others:
        if len(what_set) > 2 * len(other[2]):
            continue
        min_length = min(len(what_set), len(other[2]))
        intersection = what_set.intersection(other[2])
        rank = len(intersection)/min_length
        rank_list.append((rank, other[:1]))

    for rank_item in list(sorted(rank_list, reverse=True))[:15]:
        print(rank_item)

def main(argv):
    filename = argv[1]
    lines = []
    parsed = []

    with open(filename) as f:
        lines = f.read().split('\n')
    
    for line in lines[:-1]:
        splitted = line.split(';')
        splitted[2] = set(splitted[2].split(','))
        parsed.append(splitted)    

    compare_with_other(parsed[250], parsed)

if __name__ == "__main__":
    main(sys.argv)
