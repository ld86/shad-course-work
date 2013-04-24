#!/usr/bin/python3

from shad.book import Book
import shad.utils as utils
from shad.parallel import get_books, with_each_book
from shad.vizualization import save_dialog_picture

def work_with_book(book):
    save_dialog_picture(book, "dialogs_images/%s.png" % book.filename.replace("/", "$"))


if __name__ == "__main__":
    books_filenames = utils.get_all_books_filenames()
    books_filenames = utils.get_books_from_genre("detective")[:10]
    with_each_book(books_filenames, work_with_book, 10)
