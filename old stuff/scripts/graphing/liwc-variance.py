import csv
import numpy as np
import matplotlib.pyplot as plt
from scripts.combine import combine
from empath import Empath
from heapq import nlargest
from argparse import ArgumentParser
from scripts.graphing import common

def calc_var(metric, reports):
    return np.var(np.array([report[metric] for report in reports]))

LIWC_DATA_PATH = './articles/2018/byrace/summaries/liwc-all.csv'

if __name__ == '__main__':

    FILENAMES, LABELS, NUM_METRICS = common.get_liwc_options("liwc variance")
    reports = []
    with open(LIWC_DATA_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        labels = next(reader)
        for row in reader:
            if(row[0] in FILENAMES):
                reports.append({labels[i]:float(row[i]) for i in range(1, len(row))})

    variance = {metric: calc_var(metric, reports) for metric in reports[0].keys()}

    top_metrics = nlargest(NUM_METRICS, reports[0].keys(), key=lambda metric: variance[metric])

    for metric in top_metrics:
        print(f"{metric}: {variance[metric]}")

    data = [[report[metric] for metric in top_metrics] for report in reports]

    X = np.arange(len(top_metrics))

    for i in range(len(FILENAMES)):
        plt.bar(X + .1 * i, data[i], width = 0.1)

    plt.xticks(X, top_metrics)

    plt.legend(labels=LABELS)

    plt.show()
