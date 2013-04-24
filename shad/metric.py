class Metrics:
    def __init__(self, raw_metrics):
        self.__raw_metrics = raw_metrics

    def log_string(self):
        metrics = self.__raw_metrics[:]
        lemmas = metrics[-3]
        dialogs = metrics[-2]
        metrics[-3] = ",".join(["=".join(map(str, list(pair))) for pair in lemmas])
        metrics[-2] = ",".join(map(str, dialogs))
        return ";".join(map(str, metrics))
