#!/usr/bin/python3.2
#-*- coding: utf-8 -*-

import names_grep as ng
import glob
import os

free_class_id = 0

def corpus_handle(path):
    book_list = [fb2 for fb2 in glob.glob(path + '*.fb2*')]

    for fs_obj in os.listdir(path):
        if os.path.isdir(path + fs_obj) == True:
            book_list += corpus_handle(path + fs_obj + '/')
    
    return book_list

class Book_info:
    def __init__(self, path):
        global free_class_id
        self.name = path 
        self.class_id = free_class_id
        free_class_id += 1
        f = open(path, "rb")
        file_text = f.read()
        pure_text = ng.FB2_parser(file_text).get_text()
        ngr = ng.Names_calculator(pure_text)
        f.close()
        names_for_visual = ngr.get_names()
        names_for_visual.sort(key = lambda x: x.sort_key(), reverse = True)
        self.heroes_list = {n.name for n in names_for_visual}

def main():
    book_list = corpus_handle('corpus/')
    book_info_list = [Book_info(book) for book in book_list]
    f = open("tmp.txt", "wb")
    for book in book_info_list:
        for book2 in book_info_list:
            if book.class_id == book2.class_id:
                continue
            else:
                inter_set = book.heroes_list & book2.heroes_list
                f.write(bytes((book.name + '\n').encode('utf-8')))
                f.write(bytes((book2.name + '\n').encode('utf-8')))
                for name in inter_set:
                    f.write(bytes((name + '\n').encode('utf-8')))
                f.write(bytes(('\n' + '=============' + '\n').encode('utf-8')))
                if len(inter_set) > 50:
                    min_id = min(book.class_id, book2.class_id)
                    book.class_id = min_id
                    book2.class_id = min_id
    book_info_list.sort(key = lambda x: x.class_id)
    f.close()
    for book in book_info_list:
        print(book.name, book.class_id)

if __name__ == '__main__':
    main()
