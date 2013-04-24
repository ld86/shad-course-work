class Metrics:
    def __init__(self, raw_metrics):
        self.__raw_metrics = raw_metrics

    def get_filename(self):
        return self.__raw_metrics[0]

    def get_sentences_long(self):
        return self.__raw_metrics[1]

    def get_sentences_count(self):
        return self.__raw_metrics[2]

    def get_book_len(self):
        return self.__raw_metrics[3]

    def get_dialogs_count(self):
        return self.__raw_metrics[4]

    def get_words_len(self):
        return self.__raw_metrics[5]

    def get_words_count(self):
        return self.__raw_metrics[6]

    def get_lemmas(self):
        return self.__raw_metrics[7]

    def get_dialogs_positions(self):
        return self.__raw_metrics[8]

    def get_metric_string(self):
        metrics = self.__raw_metrics[:]
        lemmas = metrics[-3]
        dialogs = metrics[-2]
        metrics[-3] = ",".join(["=".join(map(str, list(pair))) for pair in lemmas])
        metrics[-2] = ",".join(map(str, dialogs))
        return ";".join(map(str, metrics))
