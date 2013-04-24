#!/usr/bin/python3

from shad.book import Book
import shad.utils as utils
from shad.parallel import get_books, with_each_book

def work_with_book(book):
    metrics = book.metrics()
    print(metrics.log_string())

if __name__ == "__main__":
    books_filenames = utils.get_all_books_filenames()
    with_each_book(books_filenames, work_with_book, 10)
