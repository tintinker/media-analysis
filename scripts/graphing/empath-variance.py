import numpy as np
import matplotlib.pyplot as plt
from scripts.combine import combine
from empath import Empath
from heapq import nlargest
from argparse import ArgumentParser
from scripts.graphing import common

def calc_var(metric, reports):
    return np.var(np.array([report[metric] for report in reports]))

#to call directly: python3 -m scripts.graphing.empath-basic
if __name__ == '__main__':

    DATA_PATHS, LABELS, NUM_METRICS = common.get_empath_options("empath variance")

    lexicon = Empath()

    reports = [lexicon.analyze(combine(data_path), normalize=True) for data_path in DATA_PATHS]

    variance = {metric: calc_var(metric, reports) for metric in reports[0].keys()}

    top_metrics = nlargest(NUM_METRICS, reports[0].keys(), key=lambda metric: variance[metric])

    for metric in top_metrics:
        print(f"{metric}: {variance[metric]}")

    data = [[report[metric]*100 for metric in top_metrics] for report in reports]

    X = np.arange(len(top_metrics))

    for i in range(len(DATA_PATHS)):
        plt.bar(X + .1 * i, data[i], width = 0.1)

    plt.xticks(X, top_metrics)

    plt.legend(labels=LABELS)

    plt.show()
