#!/usr/bin/python3

import sys

def file_content(file):
    # print("Readed %s" % file)
    with open(file, "rb") as f:
        return f.read()

def get_p(content):
    bs = BS(content)
    return [p.text for p in bs.select("body p")]

def main(argv):
    filename = argv[1]

if __name__ == "__main__":
    main(sys.argv)
