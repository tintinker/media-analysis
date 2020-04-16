import numpy as np
import matplotlib.pyplot as plt
from scripts.combine import combine
from empath import Empath
from heapq import nlargest
from scripts.graphing import common

#to call directly: python3 -m scripts.graphing.empath-basic
if __name__ == '__main__':
    DATA_PATHS, LABELS, NUM_METRICS = common.get_empath_options("empath top")

    lexicon = Empath()

    reports = [lexicon.analyze(combine(data_path), normalize=True) for data_path in DATA_PATHS]

    top_metrics = set()
    for report in reports:
        top_metrics.update(nlargest(NUM_METRICS, report.keys(), key=lambda key:report[key]))
    top_metrics = list(top_metrics)

    data = [[report[metric]*100 for metric in top_metrics] for report in reports]

    X = np.arange(len(top_metrics))

    for i in range(len(DATA_PATHS)):
        plt.bar(X + .1 * i, data[i], width = 0.1)

    plt.xticks(X, top_metrics)

    plt.legend(labels=LABELS)

    plt.show()
