from bs4 import BeautifulSoup as BS
from subprocess import Popen, PIPE
from sys import stderr
import re
from shad.metric import Metrics

class Book:
    def __init__(self, filename):
        self.filename = filename
        self.__mystem_re = re.compile("(.+){(.+)}")
        with open(filename, "rb") as f:
            print("> %s" % filename, file=stderr)
            self.__content = f.read()
            print("< %s" % filename, file=stderr)
        self.__p = self.__get_p(self.__content)
        self.__words = self.__mystem_process(" ".join(self.__p)).split('\n')

    def __get_p(self, content):
        bs = BS(content)
        return [p.text for p in bs.select("body p")]

    def __mystem_process(self, raw_content):
        with Popen(["./shad/mystem", "-n", "-e utf-8"], stdout=PIPE, stdin=PIPE) as pipe:
            (stdout, stderr) = pipe.communicate(bytes(raw_content, "utf-8"))
            return stdout.decode('utf-8')

    def __parse_word(self, word):
        matched = self.__mystem_re.match(word)
        if matched is None:
            return [word, ""]
        return (matched.group(1), matched.group(2))
    
    def __extract_lemmas(self):
        words = self.__words
    
        lemmas = {}

        for word in words:
            orig, lemma = self.__parse_word(word)
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
            lemmas_string.append((lemma[1], lemma[0]))

        return lemmas_string
 
    def metrics(self):
        sentences_long = 0
        sentences_count = 0
        book_len = 0
        dialogs_count = 0
        words_len = 0
        words_count = 0
        lemmas = self.__extract_lemmas()
        punctuation = 0
        current_sentence = 0
        dialogs_positions = []

        for p in self.__p:
            # Sentences work
            sentences = [sentence for sentence in p.split(".") if sentence != '']
            sentences_count += len(sentences)
            for sentence in sentences:
                sentences_long += len(sentence)

                # Dialogs count
                if  sentence.lstrip().startswith("—") or \
                    sentence.lstrip().startswith("–") or \
                    sentence.lstrip().startswith("-"):
                    dialogs_count += 1
                    dialogs_positions.append(current_sentence)

                current_sentence += 1

            # Book len
            book_len += len(p)

            # Punctuation
            for i in ",.!?;:-":
                punctuation += p.count(i)
    
        for word in self.__words:
            words_len += len(word)
        words_count = len(self.__words)
        
        return Metrics(
            [
                self.filename,
                sentences_long, 
                sentences_count, 
                book_len,
                dialogs_count,
                words_len,
                words_count,
                lemmas,
                dialogs_positions,
                punctuation                
            ])

