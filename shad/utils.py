import os
import glob

def get_all_books_filenames():
    result = []
    [result.extend(get_books_from_genre(genre)) for genre in get_all_genres()]
    return result
    
def get_books_from_genre(genre):
    return glob.glob("corpus/%s/*.fb2" % genre)

def get_all_genres():
    return os.listdir("corpus")
