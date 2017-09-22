
## ============================================================================
## Import libraries
import pandas as pd
import numpy as np
import utils
from datetime import datetime
from utils import DatePart
import sys
from urlparse import urlparse
from os.path import splitext
import random

## ============================================================================
## Constants

MIN_DATE = datetime.strptime("1/1/2009", "%m/%d/%Y")
MAX_DATE = datetime.strptime("12/30/2012", "%m/%d/%Y")
## ============================================================================
## Public methods
# getExtension
# Gets the extension
def getExtension( url ):
    """Return the filename extension from url, or ''."""
    parsed = urlparse(url)
    root, ext = splitext(parsed.path)
    return ext  # or ext[1:] if you don't want the leading '.'

## ============================================================================
## Preprocess the data
## Load apache log file dataset for a sapmle web site, who allows to be accessed
DATA = pd.read_csv("dataset/stanmoreldt.co.uk.access.log.csv")
# Delete the domain column, since the column has only one value
del DATA["domain"]
## Shuffle the data set
# Skipped||DATA = DATA.reindex(np.random.permutation(DATA.index))
## Split the data in the column datetime_offset to datetime and offset
DATA["datetime"], DATA["offset"] = DATA["datetime_offset"].str.split(" ", expand = True)
## Delete the columns which is not going to be used
del DATA["datetime_offset"]
## Extension
DATA["extension"] = DATA["page"].apply(lambda x: getExtension(x) )
## ============================================================================
# TODO: add some additional, previous items
# TODO: RE-PARSE the browsers
# TODO: Country from ip address
## ============================================================================
## Maps of the columns information
## Create maps: The data types
MAP_DATATYPE = {
    "ip":           "IP",
    "user":         "Categoric",
    "datetime":     "DateTime",
    "offset":       "Numeric",
    "action":       "Categoric",
    "page":         "Categoric",
    "http":         "Categoric",
    "returncode":   "Categoric",
    "bytes":        "Numeric",
    "referrer":     "Categoric",
    "browser":      "Short FreeText",
    "extension":    "Categoric"
}

## These values will be given by user
## UserWeight: How important this feature is.
## The sum must be "one"
## If you cannot weight them manually, then give all to equal weights (excluding ones with type none)
MAP_USERWEIGHT = {
    "ip":           0.05, 
    "user":         0.01, 
    "datetime":     0.05, 
    "offset":       0.02, 
    "action":       0.01, 
    "page":         0.05, 
    "http":         0.01, 
    "returncode":   0.05, 
    "bytes":        0.05, 
    "referrer":     0.05, 
    "browser":      0.05,
    "extension":    0.05
}

## The distances for each column
## Shows which distance is going to be used
MAP_DISTANCES = {
    "ip":           "s:IP", 
    "user":         "s:Categoric",
    "datetime":     "None", # TODO: ..
    "offset":       "None", # TODO: ..
    "action":       "s:Categoric",
    "page":         "s:Categoric",
    "http":         "s:Categoric",
    "returncode":   "s:Categoric",
    "bytes":        "n:Normalized MAPE",
    "referrer":     "s:Categoric",
    "browser":      "s:Levenshtein",
    "extension":    "s:Categoric"
}
## ============================================================================
## Declare columns and skeleton
COLUMNS = ["ip", "user", "datetime", "offset", "action", "page", "http", "returncode", "bytes", "referrer", "browser"]
SKELETON = {} # The main skeleton object to store the information about each column in the database
##  ip:             The ip address of the request
##  domain:         If the log is multi domain, it shows which domain is parsed
##  user:           If there is a login system, it shows the name of the user
##  datetime:       Date time of the visit
##  offset:         In which time domain is it?
##  action:         The action GET/POST
##  page:           The page url address
##  http:           Request type
##  returncode:     The response return code from the web server
##  bytes:          How many bytes?
##  referrer:       The referrer page url address
##  browser:        The browser which the visitor is using to browse
## ============================================================================
## Declare Info Class
class Info:
    def __init__( self, dataset, column ):
        self.column = column
        self.dataset = dataset
        self.std = None

    def getTermValue( self, input ):
        return random.random()
#    def getTermPropotion( self, input ):
#        return random.random() / 2.0
    def getStandardDeviation( self ):
        if self.std == None:
            self.std = self.dataset[ self.column ].std()
        return self.std

## Create skeleton from data
for c in DATA:
    # General type and weight
    SKELETON[ c ] = { 
            'UserWeight': MAP_USERWEIGHT[ c ], 
            'Type': str(DATA.dtypes[c]), 
            'DataType': MAP_DATATYPE[ c ], 
            'Distance': MAP_DISTANCES[ c ],
            'Weight': 1.0} # TODO: calculate the weight

    SKELETON[ c ]['Info'] = Info( DATA, c )
    # Frequency table
    freq = DATA[ c ].value_counts().to_dict()
    for v in freq:
        freq[v] = float(freq[v]) / float(len(DATA))
    SKELETON[ c ]['FrequencyTable'] = freq






from collections import Counter
from pandas import DataFrame
import operator

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



fw = FeatureWeight( DATA, {"bytes":10} )
scores = fw.scores(fw.frequencies())
for c in scores:
    SKELETON[ c ]["Weight"] = scores[c]
   




"""
import matplotlib.pyplot as plt

ds = DATA.head(100)

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

fw = feature_weights.FeatureWeight(ds, {"noagent":5, "find":5, "crawler":10})

print fw.weights()["ip"]

"""
7
