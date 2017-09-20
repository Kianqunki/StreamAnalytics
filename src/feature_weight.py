'''
Calculates anomaly score based on distribution of the provided dataset
Refer to anomaly_score_test for usage guide
'''
from collections import Counter
import numpy as np
from pandas import DataFrame

class FeatureWeight(object):
    '''
    This class is used for finding frequency based weight scores of feature in a dataset
    '''
    def __init__(self, data, numeric_bins):
        if not isinstance(data, DataFrame):
            raise ValueError("data should be of dataframe type")
        self.__data__ = data
        self.__bins__ = numeric_bins

    def frequencies(self):
        '''
        Finds frequencies of features in the dataset.

        Returns:
            returns (dict)
                    keys    : feature name
                    values  : tuple (frequency, distinct value)
        '''
        feature_frequencies = {}
        for column in self.__data__.columns:
            if self.__bins__ is not None and column in self.__bins__:
                frequencies = self.__find_numeric_frequencies__(column)
            else:
                frequencies = self.__find_nonnumeric_frequencies__(column)
            feature_frequencies[column] = sorted(frequencies, reverse=True)
        return feature_frequencies

    def scores(self, frequencies):
        ''' calculates weight score for each feature

        Args:
            frequencies (dict) : return value of frequencies function

        Returns:
            returns (dict)
                    keys   : feature name
                    values : weight score
        '''
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


# FUNCTIONALITY TEST
# from datasets.edgar import edgar
from datasets.stanmore import stanmore
import matplotlib.pyplot as plt
import operator

# ds = edgar.DATASET.head(100)
ds = stanmore.DATASET

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

def test_frequencies():
    fw = FeatureWeight(ds, {"bytes":10})
    print fw.frequencies()

def test_frequencies_by_feature(feature):
    fw = FeatureWeight(ds, {"bytes":10})
    print fw.frequencies()[feature]

def test_scores():
    fw = FeatureWeight(ds, {"bytes":10})
    print fw.scores(fw.frequencies())

def test_scores_by_feature(feature):
    fw = FeatureWeight(ds, {"bytes":10})
    print fw.scores(fw.frequencies())[feature]

def plot_scores():
    fw = FeatureWeight(ds, {"bytes":10})
    scores = fw.scores(fw.frequencies())
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    zipped_scores = zip(*sorted_scores)
    features = zipped_scores[0]
    values = zipped_scores[1]
    n_features = range(1, len(features) + 1)
    plt.bar(n_features, values, width=0.8, color="b", align="center")
    plt.xticks(n_features, features)
    plt.show()

plot_scores()