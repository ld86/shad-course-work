#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import itertools
import urllib.request
from bs4 import BeautifulSoup as BS
import os
from multiprocessing import Pool

genres = \
    [
        "det_action",
        "detective",
        "thriller",
        "children",
        "child_prose",
        "child_sf",
        "love_history",
        "love_contemporary",
        "prose_history",
        "prose_rus_classic",
        "prose_su_classics",
        "prose_contemporary",
        "religion_rel",
        "sf_history",
        "sf_action",
        "sf",
        "sf_fantasy",
        "humor_prose"
    ]

def main():
    list(map(download_genre, genres))

def download_genre(genre):
    links = extract_book_links(genre)
    download_books(links, genre)

def download_books(links, genre):
    if not os.path.exists(genre):
        os.mkdir(genre)

    pool = Pool(2)
    pool.map(download_book, zip(links, itertools.repeat(genre)))
    pool.close()
    pool.join()

def download_book(link_and_genre):
    (link, genre) = link_and_genre
    print("Try download %s %s" % (genre, link))
    save_book(link, "%s/%s" % (genre, link.replace("/","$")))
    time.sleep(10)

def extract_book_links(genre):
    bs = BS(get_genre_page(genre))
    links = []
    for a in bs.select("ol a"):
        if len(links) == 100:
            break
        if "/b/" in a["href"]:
            links.append(a["href"])
    return links

def save_book(book, path):
    url = "http://flibusta.net" + book + "/fb2"
    try:
        urllib.request.urlretrieve(url, path) 
    except Exception as e:
        print(e)
        print("Skip %s" % book)

def get_genre_page(genre):
    url = "http://flibusta.net/g/%s/Pop" % genre
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    request = urllib.request.Request(url, headers=headers)
    return urllib.request.urlopen(request).read().decode('utf-8')

if __name__ == "__main__":
    main()
