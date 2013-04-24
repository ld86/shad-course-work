from multiprocessing import Pool
from shad.book import Book
from itertools import repeat

def get_book(filename):
    return Book(filename)

def each_book(filename_and_worker):
    filename, worker = filename_and_worker
    worker(Book(filename))

def with_each_book(filenames, worker, concurrency):
    pool = Pool(concurrency)
    pool.map(each_book, zip(filenames, repeat(worker)))
    pool.close()
    pool.join()

def get_books(filenames, concurrency):
    pool = Pool(concurrency)
    books = pool.map(get_book, filenames)
    pool.close()
    pool.join()
    return books
