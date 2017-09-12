# NOTE: Please note that, to change the distance function of k-means there are two 
# ways. First way is to override the distance function by pointing the distance function to a function
# e.g.: 
# def myfunc(a, b):
#   pass
# kmeans = sklearn.Kmeans()
# kmeans.distance_function = myfunc
# But most of the useful libraries are not capable of overriding function (they do not allow)
# So, it is better to have a "pure" kmeans implemetation in python then override the distance function
# Our aim is not modifying the k-means core. Our aim is to make an adaptive distance algorithm.

#############################################################################
# Full Imports


import math
import random
import utils
import numpy as np
import time
import pandas as pd

import data # This is our module
import distance # This is our module
from anomaly_score import AnomalyScore

import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')
from pandas.tools.plotting import parallel_coordinates

anomaly_scoring = AnomalyScore(data.SKELETON)
anomaly_scoring.fit(data.DATA)

def anomalyScore(row):
    # NOTE UGUR/OZKAN HOCAM
    # Buraya ilgili anomaly degerini ureten fonksiyonu baglamak lazim
    anomaly_scores = anomaly_scoring.predict(row)
    return anomaly_scores[0]

class Cluster:

    # Cluster
    # @centroid: The input centroid of the cluster
    # @completed
    def __init__( self, centroid ):
        self.points = []
        self.centroid = centroid
        self.points.append( centroid )

    # getDistance
    # Returns the distance with the cluster and row
    # @row: The target row to be checked
    # @return: The distance to the row
    # @completed
    def getDistance( self, row ):
        dis = 100000000000.0
        for i in range(len(self.points)):
            c = self.points[i]
            d = distance.mixeddistance( c, row, data.SKELETON )
            if d < dis:
                dis = d
        return dis

    def findWeakest( self ):
        if len(self.points) < 5:
            raise Exception("Must be at least 5 items")

        mindis = 10000000000000.0
        minind = -1
        for i in range(len(self.points)):
            dis = 0
            for j in range(len(self.points)):
                dis = dis + distance.mixeddistance( self.points[i], self.points[j], data.SKELETON )
            if dis < mindis:
                mindis = dis
                minind = i

        # Return
        return minind

    # appendItem
    # Appends an item to points
    # @row: The newly added row
    def appendItem( self, row ):
        # Append it to points
        self.points.append( row )
        # Check if it contains more than limit
        if len(self.points) > CLUSTER_SIZE:
            # we need to remove some items
            index = self.findWeakest( )
            del self.points[index]
            #self.points = np.delete(self.points, index)

# Declare some initial parameters
NUM_CLUSTERS = 10
clusters = []
ANOMALY_RANGE = 4.000
CLUSTER_SIZE = 10

# Create clusters from randomly selected points
for i in range(NUM_CLUSTERS):
    index = random.randint( 0, len(data.DATA) - 1 )
    cluster = Cluster( data.DATA.iloc[index] )
    for j in range(CLUSTER_SIZE - 1):
        index = random.randint( 0, len(data.DATA) - 1 )
        cluster.appendItem( data.DATA.iloc[index] )
    clusters.append( cluster )

# Assign items to the cluster
for i in range(100): # len(data.DATA)
    # Wait
    if i % 50 == 0 and i > 0:
        time.sleep(1)

    # Pick the ith item
    row = data.DATA.iloc[i]
    if row is None:
        print "There is an item which is None"
    else:
        # Find the anomaly point
        an = anomalyScore( row )
        if an < ANOMALY_RANGE:

            # Find the cluster which is closest to the point
            mindis = 100000000000.0
            minind = -1
            for j in range(len(clusters)):
                dis = clusters[j].getDistance( row )
                if dis < mindis:
                    mindis = dis
                    minind = j

            # Assign the item to the cluster for updating
            if minind > -1:
                clusters[minind].appendItem( row )

            # Report
            print "Item [", i, "] is assigned to the cluster [", minind, "] with the distance:", mindis
        else:
            print "Item [", i, "] is an anomaly with a distance of", an


cols = list(data.DATA.columns)
cols.append("class")

clusters_df = pd.DataFrame(index = None, data = None, columns = cols)
for j in range(len(clusters)):
    for i in range(10):
        l = clusters[j].points[i].tolist()
        l.append( str(j) )
        clusters_df.loc[ len(clusters_df) ] = l

max_value = np.max(clusters_df.max(numeric_only=True))/4
print max_value

for c in clusters_df:
    if c != 'class':
        if data.SKELETON[c]['DataType'] == 'None' or \
           data.SKELETON[c]['DataType'] == 'Date' or \
           data.SKELETON[c]['DataType'] == 'Ordinal' or \
           data.SKELETON[c]['DataType'] == 'Short FreeText':
            del clusters_df[c]
            cols.remove(c)
        elif data.SKELETON[c]['DataType'] == 'Categoric':
            clusters_df[c] = pd.Categorical(clusters_df[c])
            new_column = "c" + c
            codes = clusters_df[c].cat.codes
            clusters_df[new_column] = [max_value/len(codes)*code for code in codes]
            cols.append(new_column)
            cols.remove(c)
            
import pandas.util.testing as tm

cols.remove("class")
parallel_coordinates(clusters_df, "class", cols=cols)
plt.show()