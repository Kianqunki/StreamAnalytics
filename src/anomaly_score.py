'''
Calculates anomaly score based on distribution of the provided dataset
Refer to anomaly_score_test for usage guide
'''
from collections import Counter
import numpy as np
import pandas as pd
from pandas import DataFrame

class AnomalyScore(object):
    ''' Calculates anomaly score based on distribution of the provided dataset

    Args:
        skeleton     (skeleton) : dataset metadata
    '''
    def __init__(self, skeleton):
        self.__skeleton__ = skeleton
        self.__data__ = None
        self.__distributions__ = {}
        self.__histogram_handlers__ = {
            "Numeric" : self.__bin_histogram_handler__,
            "Categoric" : self.__categoric_histogram_handler__,
            "Ordinal" : self.__categoric_histogram_handler__,
            "Short FreeText" : self.__categoric_histogram_handler__,
            "Date" : self.__date_histogram_handler__
        }

    def fit(self, data):
        ''' calculates distribution of each dataset feature

        Args:
            data     (DataFrame) : dataset

        Returns:
            returns distributions of each dataset feature
        '''
        if not isinstance(data, DataFrame):
            raise ValueError("dataset should be of dataframe type")

        self.__data__ = data

        for column in self.__data__.columns:
            datatype = self.__skeleton__[column]["DataType"]
            if datatype in self.__histogram_handlers__:
                column_distributions = self.__histogram_handlers__[datatype](data, column)
                self.__distributions__[column] = column_distributions
        return self.__distributions__

    def predict(self, data):
        ''' generates instance-wise anomaly score for each feature

        Args:
            data     (DataFrame/Series) : dataset

        Returns:
            returns anomaly scores in DataFrame type
        '''
        if isinstance(data, pd.Series):
            data = pd.DataFrame([data])

        predictions = None
        for column in data.columns:
            scores = []
            values = data[column]
            datatype = self.__skeleton__[column]["DataType"]
            if datatype in self.__histogram_handlers__:
                for value in values:
                    if datatype == "Numeric":
                        scores.append(self.__find_bin_score__(column, value))
                    elif datatype == "Categoric" or \
                        datatype == "Ordinal" or   \
                        datatype == "Short FreeText":
                        scores.append(self.__find_categoric_score__(column, value))
                    elif datatype == "Date":
                        scores.append(self.__find_bin_score__(column, value))
                    else:
                        pass
                if predictions is None:
                    predictions = DataFrame({column : scores})
                else:
                    predictions[column] = scores
        
        anomaly_scores = []
        for row in predictions.iterrows():
            values = [value + 0.0001 for value in row[1]]
            anomaly_scores.append(np.prod(values))
        return anomaly_scores

    def __bin_histogram_handler__(self, data, column):
        column_bins = self.__skeleton__[column]["bins"]
        proba_density, bins = np.histogram(data[column], column_bins)
        total = np.sum(proba_density)
        density = [float(i)/total for i in proba_density]
        return ([1 - i for i in density] , bins)

    def __categoric_histogram_handler__(self, data, column):
        values = data[column]
        count_values = len(values)
        category_dist = Counter(values)
        density = []
        categories = []
        for category in category_dist:
            density.append(1 - category_dist[category]/float(count_values))
            categories.append(category)
        return (density, categories)

    def __date_histogram_handler__(self, data, column):
        dates = data[column]
        date_bins = self.__skeleton__[column]["bins"]
        density = [0.0] * len(date_bins)
        for date in dates:
            for index, bin_item in enumerate(date_bins):
                if index < len(date_bins) - 2:
                    if date >= bin_item and date < date_bins[index + 1]:
                        density[index] += 1.0
                        break
                else:
                    if date >= bin_item and date <= date_bins[index + 1]:
                        density[index] += 1.0
                    break
        return ([1.0 - (float(x)/len(dates)) for x in density] , date_bins)


    def __find_bin_score__(self, column, value):
        column_distribution, bins = self.__distributions__[column]
        index = 0
        for index, bin_item in enumerate(bins):
            if index < len(bins) - 2:
                if value >= bin_item and value < bins[index + 1]:
                    return column_distribution[index]
            else:
                if value >= bin_item and value <= bins[index + 1]:
                    return column_distribution[index]
                return None

    def __find_categoric_score__(self, column, value):
        column_distribution, bins = self.__distributions__[column]
        for index, bin_item in enumerate(bins):
            if value == bin_item:
                return column_distribution[index]
        return None

    @property
    def distributions(self):
        ''' Feature distribtions '''
        return self.__distributions__
