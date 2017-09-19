'''
Calculates anomaly score based on distribution of the provided dataset
Refer to anomaly_score_test for usage guide
'''
from collections import Counter
import numpy as np
from pandas import DataFrame

class FeatureWeight(object):
    def __init__(self, data, numeric_bins):
        if not isinstance(data, DataFrame):
            raise ValueError("data should be of dataframe type")
        self.__data__ = data
        self.__bins__ = numeric_bins

    def frequencies(self, reversed=False):
        feature_frequencies = {}
        for column in self.__data__.columns:
            if self.__bins__ is not None and column in self.__bins__:
                frequencies = self.__find_numeric_frequencies__(column)
            else:
                frequencies = self.__find_nonnumeric_frequencies__(column)
            feature_frequencies[column] = sorted(frequencies, reverse=True)
        return feature_frequencies

    def scores(self, frequencies):
        scores_ = {}      
        for f in frequencies:
            fs = frequencies[f]
            if fs[0][0] >= 1.0:
                scores_[f] = 0.0                
                continue
            score = fs[0][0]
            for idx, s in enumerate(fs):
                score = score / (1/(1-(fs[idx][0]-fs[idx+1][0])))
                if idx >= 4 or idx + 1 >= len(fs) - 1:
                    break
            scores_[f] = score
        return scores_

    def __find_numeric_frequencies__(self, column):
        num_of_bins = self.__bins__[column]
        values = self.__data__[column]
        proba_density, bins = np.histogram(values, bins=num_of_bins)
        total = np.sum(proba_density)
        frequencies = [(float(val)/total, bins[idx]) for idx, val in enumerate(proba_density)]
        return frequencies

    def __find_nonnumeric_frequencies__(self, column):
        data = self.__data__[column]
        count_values = len(data)
        value_occurances = Counter(data)
        frequencies = []
        for value in value_occurances:
            frq = value_occurances[value]/float(count_values)
            frequencies.append((frq, value))
        return frequencies

from datasets.edgar import edgar
import matplotlib.pyplot as plt

ds = edgar.DATASET.head(100)

def plot_weight(weights, feature):
    wg = weights[feature]
    zipped = zip(*wg)

    X = range(len(zipped[1]))
    Y = zipped[0]

    fig, ax = plt.subplots()
    ax.plot(X, Y, "-o")

    for i, lbl in enumerate(zipped[1]):
        ax.annotate(lbl, (X[i], Y[i]), textcoords="offset points", horizontalalignment="right", verticalalignment="bottom")

    plt.title("".join([feature, " weights"]))
    plt.show()

fw = FeatureWeight(ds, {"noagent":5, "find":5, "crawler":10})
# plot_weight(fw.frequencies(), "ip")
freqs = fw.frequencies()

# print freqs
# print fw.scores(freqs)

print freqs["ip"]
print fw.scores(freqs)["ip"]