# -*- coding: utf-8 -*-
"""
Created on Wed Sep 06 08:11:11 2017

@author: eyazici
"""
# =============================================================================
#| Imports

import random # randomization operations
import math # Mathematical operations
import numpy as np # Numerical operations
from scipy.stats import norm # Statistical operations
import distance # Our own distance module
import data # Our own data module
# =============================================================================
#| Public Functions

# log
# Logs the data
# @message: The input message
#@skiplines: CRLF
# @completed
def log( message, skiplines = False ):
    if skiplines:
        print message,
    else:
        print message

# distance
# This function is a distance metric
# @a: The first item
# @b: The second item
# @return: Distance
def itemDistance( a, b ):
    return distance.mixeddistance( a, b, data.SKELETON )

def itemDistanceDesc( a, b ):
    return distance.mixeddistance( a, b, data.SKELETON, withDesc = True )
# =============================================================================
#| Private Functions
    
# __generateRowFromList__
# Generates (transforms) row from a list
# @inlist: The input list
# @return: Tuple
# @completed
def __generateRowFromList__( inlist ):
    #: Return
    return tuple(inlist)

# __generateRowFromDict__    
# Generates (transforms) row from a dict
# @indict: The input dict
# @return: Tuple
# @completed
def __generateRowFromDict__( indict ):
    #: Return
    return tuple( indict.values() )

# __generateRandomItem__
# Generates random item
# @length: The item length
# @bias: The bias to be added to the values
# @return: A tuple of randomly valued row
# @completed
def __generateRandomItem__( length, bias = 0.0 ):
    #: Generate & return
    return __generateRowFromList__([ (round(random.random(), 2) + bias) for x in range(length)])

# __generateRandomItems__
# Generates random items, like a dataset
# @count: The number of items to generate
# @length: The length of each item
# @bias: The bias to be added to the values
# @return: Array of tuples
# @completed
def __generateRandomItems__( count, length, bias = 0.0 ):
    return [ __generateRandomItem__( length, bias ) for x in range(count) ]

# =============================================================================
#| Constants
MIN_ITEMCOUNT = 5
DISTANCE_POWER = 3

# =============================================================================
#| Classes

# Class: Cluster
# Cluster class
class Cluster(object):
    
    # __str__
    # @completed
    def __str__( self ):
        return "Cluster.#" + str(len(self.items))

    # __init__
    # @completed
    def __init__( self ):
        #: Set items
        self.items = []
        #: Distance matrix
        self.distMatrix = {}
        
    # internalDistance
    # Calculates the internal distance
    # @return: The distance
    # @completed
    def internalDistance( self ):
        #: Define variables
        d = 0.0 # total distance
        c = 0 # how many items 
        #: Loop
        for i in range(len(self.items)):
            #: Loop for each item to find similarities
            for j in range(len(self.items)):
                #: If they are not same
                if i != j:
                    #: Calculate
                    d += pow( itemDistance( self.items[i], self.items[j] ), DISTANCE_POWER )
                    #: Increment the count
                    c += 1
        #: Return
        return round(math.sqrt( d / float( c ) ), 2)

    # append
    # Appends an item to cluster
    # @item: The input item
    # @completed
    def append( self, item ):
        #: Append item to it items
        self.items.append( item )
        #: Optimize
        self.optimize()

    # optimize
    # Optimizes the items by removing the most central (worst) one
    # @completed
    def optimize( self ):
        #: Check that, do we really need to remove it?
        while len(self.items) > MIN_ITEMCOUNT:
            #: Find the worst item
            index = self.__findWorst__()
            #: Delete the item
            if index != None:
                # TODO: should not be using this clause
                del self.items[ index ]
            #: If somehow none has come, break it
            elif index == None:
                break

    # __findWorst__
    # Finds the worst item: Definition of worst => closest item to others
    # @completed
    def __findWorst__( self ):
        #: Declare variables
        minimum = 100000000000.0
        minitemindex = None
        #: Loop for each item
        for i in range(len(self.items)):
            #: Declare variables
            d = 0.0
            #: Loop for each item to find similarities
            for j in range(len(self.items)):
                #: If they are not same
                if i != j:
                    #: Calculate
                    thecalculateddistance = 0.0
                    
                    #!! memory
                    if len(self.distMatrix) > 60:
                        self.distMatrix = {}
                    
                    s1 = str(self.items[i])
                    s2 = str(self.items[j])
                    ss = s1 + "|" + s2
                    
                    if ss in self.distMatrix:
                        thecalculateddistance = self.distMatrix[ ss ]
                    else:                   
                        thecalculateddistance = pow( itemDistance( self.items[i], self.items[j] ), DISTANCE_POWER )
                        self.distMatrix[ ss ] = thecalculateddistance 
                        
                    d += thecalculateddistance
            #: Check
            if d < minimum:
                #: Set minimum
                minimum = d
                #: Set item
                minitemindex = i
        #: Return the index
        return minitemindex

    # dist
    # Finds the distance of given item
    # @item: The item to be measured
    # @matrix: The distance matrix
    # @return: The minimum distance
    # @completed
    def dist( self, item ):
        #: Define variables
        minimum = 100000000000
        #: Loop for each item
        for i in range(len(self.items)):
            #: Re-Set value
            d = 100000000000
            #: Get the distance
            d = itemDistance( self.items[i], item )
            if d < minimum:
                minimum = d
        #: Return the minimum
        return minimum

    # distWithDesc
    # Finds the distance of given item
    # @item: The item to be measured
    # @matrix: The distance matrix
    # @return: The minimum distance
    # @completed
    def distWithDesc( self, item ):
        #: Define variables
        minimum = 100000000000
        desc = None
        #: Loop for each item
        for i in range(len(self.items)):
            #: Re-Set value
            d = 100000000000
            #: Get the distance
            d = itemDistance( self.items[i], item )
            if d < minimum:
                minimum = d
                desc = itemDistanceDesc( self.items[i], item )
        #: Return the minimum
        return desc  

# class: EUO
# The main clusterer class
class EUO(object):
    
    # __str__
    # @completed
    def __str__( self ):
        #: Declare variables
        s = "|"
        #: Accumulate the string
        for c in self.clusters:
            s = s + str(c.internalDistance()) + "|"
        #: Return
        return s

    # __init__
    # @clustercount: The number of clusters to build
    # @completed
    def __init__( self, clustercount = 10 ):
        #: Define clusters
        self.clusters = []
        #: Define stack
        self.stack = []
        #: Assign cluster count
        self.clustercount = clustercount
        #: Watches
        self.__watches__ = []
        #: Statistics
        self.__mean__ = 0
        self.__std__ = 0
        self.__per80__ = 0
        self.__per90__ = 0
        self.__per95__ = 0
        self.__per98__ = 0
        self.__per99__ = 0
        self.__per992__ = 0
        self.__per995__ = 0
        self.__per997__ = 0
        self.__per999__ = 0

    # push
    # Pushes an item to stack and make clusters
    # @item: The input item
    # @completed
    def push( self, item ):
        
        #: If there are no clusters
        if len(self.clusters) == 0:
            #: If there are not enough items in stack
            if len(self.stack) < self.clustercount * MIN_ITEMCOUNT:
                #: Push to stack
                self.stack.append( item )
            else:
                #: Build the clusters
                self.__buildClusters__()
        else:
            #: Assign it to most appropriate cluster
            self.__assign__( item )

    # __findClosestCluster__
    # Finds the closest cluster
    # @item: The item to be measured
    # @matrix: The 
    def __findClosestCluster__( self, item ):
        #: Define variables
        minitem = None
        minimum = 100000000000
        #: Loop for each cluster
        for j in range(len(self.clusters)):
            #: Measure the distance
            d = self.clusters[j].dist( item  )
            #: If it is the minimum
            if d < minimum:
                #: Set the item and distance
                minimum = d
                minitem = j
        #: Return
        return minitem
        
    # __buildClusters__
    # Builds the clusters
    # @completed
    def __buildClusters__( self ):
        log(">> building clusters")
        #: Define variables
        selected = []
        #: Select a random item
        itemindex = random.randint(0, len(self.stack) - 1)
        #: Create a cluster
        cluster = Cluster( )
        #: Assign item to it
        cluster.append( self.stack[itemindex] )
        #: Add the item to selected (exclude)
        selected.append( itemindex )
        #: Add the cluster to clusters
        self.clusters.append( cluster )
        #: Loop until necessary clusters are completed
        while len(self.clusters) < self.clustercount:
            log(">> cluster count:" + str(len(self.clusters))  + "; selected count:" + str(len(selected)))
            #: Get an item which is far away from all others
            itemindex = self.__farestDistance__( selected )
            #: If not selected
            if itemindex not in selected:
                #: Create a cluster
                cluster = Cluster()
                #: Assign the item to it
                cluster.append( self.stack[itemindex] )
                #: Add the item to selected (exclude)
                selected.append( itemindex )
                #: Add the cluster to clusters
                self.clusters.append( cluster )
        log(">> clusters built, assigning items")
        #: For the remaining ones
        for i in range(len(self.stack)):
            #: If it is not currently assigned
            if i not in selected:
                log(str(i), True)
                #: Find the closest
                closest = self.__findClosestCluster__( self.stack[i] )
                #: Assign it to cluster
                self.clusters[ closest ].append( self.stack[i] )
                #: Add it to big list
                selected.append( i )
        log("")
        log(">> items are assigned to the clusters")

    # __farestDistance__
    # Finds the item which is farest of the given @items
    # @items: The items to be avoided
    # @return: The index of the item
    # @completed
    def __farestDistance__( self, items ):
        #: Declare variables
        maximum = 0.0
        maxitem = None
        #: Loop for each item in stack
        for i in range(len(self.stack)):
            #: Re-Set value
            dist = 0
            #: For each given item
            for j in items:
                #: Get the distance
                dist += itemDistance( self.stack[i], self.stack[j] )
            #: If the distance is maximum and i is not in items (selected)
            if dist > maximum and i not in items:
                #: Set maximum
                maximum = dist
                #: Set index
                maxitem = i
        #: Return index
        return maxitem
    
    # evaluate
    # Evaluates the item (how far is it to the dataset)
    # @item: The input item
    # @return: The score as the distance, bigger value is worse
    # @completed
    def evaluate( self, item, withDesc = False ):
        #: Define variables
        minimum = 100000000000
        mindesc = None
        #: Loop for each cluster
        for j in range(len(self.clusters)):
            #: Measure the distance
            d = self.clusters[j].dist( item )
            #: If it is the minimum
            if d < minimum:
                #: Set the item and distance
                minimum = d
                if withDesc == True:
                    mindesc = self.clusters[j].distWithDesc( item )
                
        #: Return minimum
        if minimum > self.__per999__:
            return (0.999, mindesc)
        elif minimum > self.__per997__:
            return (0.997, mindesc)
        elif minimum > self.__per995__:
            return (0.995, mindesc)
        elif minimum > self.__per992__:
            return (0.992, mindesc)
        elif minimum > self.__per99__:
            return (0.99, mindesc)
        elif minimum > self.__per98__:
            return (0.98, mindesc)
        elif minimum > self.__per95__:
            return (0.95, mindesc)
        elif minimum > self.__per90__:
            return (0.90, mindesc)
        elif minimum > self.__per80__:
            return (0.80, mindesc)
        return (0, None) # norm.pdf( minimum, self.__mean__, self.__std__ )
    
    # watch
    # Watches the item scores (how far is it to the dataset)
    # @item: The input item
    # @completed
    def watch( self, item ):
        #: Define variables
        minimum = 100000000000
        #: Loop for each cluster
        for j in range(len(self.clusters)):
            #: Measure the distance
            d = self.clusters[j].dist( item )
            #: If it is the minimum
            if d < minimum:
                #: Set the item and distance
                minimum = d
        #: Add watches
        self.__watches__.append( round(minimum, 3) )

    # endWatch
    # Ends the watching phase
    def endWatch( self ):
        a = np.array( self.__watches__ )
        self.__mean__ = np.mean( a )
        self.__std__ = np.std( a )
        self.__per80__ = np.percentile( a, 80.0 )
        self.__per90__ = np.percentile( a, 90.0 )
        self.__per95__ = np.percentile( a, 95.0 )
        self.__per98__ = np.percentile( a, 98.0 )
        self.__per99__ = np.percentile( a, 99.0 )
        self.__per992__ = np.percentile( a, 99.2 )
        self.__per995__ = np.percentile( a, 99.5 )
        self.__per997__ = np.percentile( a, 99.7 )
        self.__per999__ = np.percentile( a, 99.9 )

    # __assign__
    # Assigns the item to appropriate cluster
    # @item: The input item
    # @completed
    def __assign__( self, item ):

        #: Define variables
        minitem = None
        minimum = 100000000000
        #: Loop for each cluster
        for j in range(len(self.clusters)):
            #: Measure the distance
            d = self.clusters[j].dist( item )
            #: If it is the minimum
            if d < minimum:
                #: Set the item and distance
                minimum = d
                minitem = j
        #: Assign it to minimum item
        self.clusters[minitem].append( item )

# =============================================================================
# =============================================================================
# =============================================================================






# =============================================================================
# =============================================================================
# START POINT
# =============================================================================
# =============================================================================

# __generateItem__
# Randomly picks an item from dataset
# @return: Random row
# @completed
def __generateItem__( ):
    return dict(data.DATA.loc[ random.randint(0, len(data.DATA)-1) ])
   

# PHASE 1:
# Create the clusters from the data
log(">> pushing items")
euo = EUO( 4 )
for i in range(100):
    if i % 20 == 0 and i > 0:
        log(str(i))
    else:
        log(str(i), True)
    #: Push the item
    euo.push( __generateItem__() )

print euo

for c in euo.clusters:
    print "Cluster: ", c

# PHASE 2:
# Watch the scores
log(">> pushing watch items")
for i in range(50):
    if i % 10 == 0:
        log(">> " + str(i))
    row = __generateItem__()
    euo.watch( row )
euo.endWatch()

print "Mean", euo.__mean__
print "0.999", euo.__per999__
print "0.99", euo.__per99__
print "0.80", euo.__per80__

log(">> end watch is trigged")

# PHASE 3:
# Evaluate the distance
for i in range(100):
    row = __generateItem__()
    evaluation = euo.evaluate( row )
    print "==========================================="
    if evaluation > 0.8:
        print evaluation
        print str(row)
        print euo.evaluate( row, True )

# =============================================================================


>> pushing items
0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
>> building clusters
>> cluster count:1; selected count:1
>> cluster count:2; selected count:2
>> cluster count:3; selected count:3
>> clusters built, assigning items
0 1 2 3 4 5 6 8 9 10 11 12 13 14 16 17 
>> items are assigned to the clusters
21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40
41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60
61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80
81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 |726.54|342.41|665.82|250.57|
Cluster:  Cluster.#5
Cluster:  Cluster.#5
Cluster:  Cluster.#5
Cluster:  Cluster.#5
>> pushing watch items
>> 0
>> 10
>> 20
>> 30
>> 40
Mean 14.17082
0.999 47.055702
0.99 45.82002
0.80 31.7092
>> end watch is trigged
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 30569, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/event-photo.jpg', 'browser': 'Mozilla/5.0 (iPhone; CPU iPhone OS 5_1_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9B206 Safari/7534.48.3'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Alucobond.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=532', 'action': 'GET', 'page': '/perch/core/assets/js/dropzone.js?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '66.249.93.84', 'offset': 1, 'bytes': 8522, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Downer.gif', 'browser': 'Mozilla/5.0 (Linux; Android 4.3; Build/LPV79) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.94 Mobile Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 1055, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/js/main.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 175, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=529', 'action': 'GET', 'page': '/perch/core/assets/js/jquery-ui.js?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 184231, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/glazing/', 'action': 'GET', 'page': '/perch/resources/01-24.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Knopp.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 366151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/drylining/waterside-park-north-woolwich-road-the-royal-docks-london.php', 'action': 'GET', 'page': '/perch/resources/04-28.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 40.210083380368594, 'user': 0.0, 'referrer': 0.00874571640403193, 'action': 0.0003679575550085889, 'page': 0.001298874634321687, 'browser': 0.0033729622988998434})
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '195.162.126.18', 'offset': 1, 'bytes': 7236, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/contact.php', 'action': 'GET', 'page': '/perch/resources/telephone.png', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18'}
(0, None)
===========================================
(0.999, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 2100615, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/divisions/drylining-1.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
(0.999, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.0, 'bytes': 105.07442280584446, 'user': 0.0, 'referrer': 0.006855643755271653, 'action': 0.0003679575550085889, 'page': 0.0012966975467513554, 'browser': 0.004426255096912737})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/templates/generic.php', 'action': 'GET', 'page': '/img/Customers/Alucobond.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 1027, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/', 'action': 'GET', 'page': '/perch/core/inc/js_privs.php', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 10762, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/stanmore-logo-established-1958.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/assurances/training.php', 'action': 'GET', 'page': '/img/Customers/Cemex.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 152, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/dry-lining.php', 'action': 'GET', 'page': '/img/Customers/kingspan.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '153.98.68.197', 'offset': 1, 'bytes': 8522, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Downer.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 5086, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/?id=19', 'action': 'GET', 'page': '/perch/core/apps/content/edit/?id=530', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00707945504582416, 'ip': 0.01073912363591437, 'bytes': 35.901709656789336, 'user': 0.0, 'referrer': 0.0069498169554284145, 'action': 0.0003679575550085889, 'page': 0.0012816998323779605, 'browser': 0.00614862919070284})
===========================================
(0.95, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '80.169.95.30', 'offset': 1, 'bytes': 4398, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/perch/resources/smartsystems.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.95, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 44.116571133070387, 'user': 0.0, 'referrer': 0.006813926679763613, 'action': 0.0003679575550085889, 'page': 0.0012813974591043033, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 1535, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=44', 'action': 'GET', 'page': '/perch/core/apps/assets/async/get-assets.php?page=1&type=img&_=1405359961618', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.99, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 4084, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/templates/division.php', 'action': 'GET', 'page': '/templates/generic.php', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.99, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.007427632596897634, 'ip': 0.01073912363591437, 'bytes': 45.866608032851929, 'user': 0.0, 'referrer': 0.008874584993720132, 'action': 0.0003679575550085889, 'page': 0.0012973627679534012, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/js/vendor/modernizr-2.6.2.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 597, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=74', 'action': 'GET', 'page': '/perch/addons/plugins/editors/markitup/images/markdown/link.png', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.007680387156032522, 'ip': 0.005369561817957185, 'bytes': 33.316626559558102, 'user': 0.0, 'referrer': 0.008865911146337271, 'action': 0.0003679575550085889, 'page': 0.0012921619476464982, 'browser': 0.0})
===========================================
(0.9, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '66.249.64.145', 'offset': 1, 'bytes': 388057, 'datetime': 0, 'user': '-', 'referrer': '-', 'action': 'GET', 'page': '/img/Customers/Eurofox.jpg', 'browser': 'Googlebot-Image/1.0'}
(0.9, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 43.461377117926673, 'user': 0.0, 'referrer': 0.008261633111998049, 'action': 0.0003679575550085889, 'page': 0.0012988141596669556, 'browser': 0.008758423524311505})
===========================================
(0.999, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 391, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=46', 'action': 'POST', 'page': '/perch/core/apps/assets/upload/', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.999, {'returncode': 0.0003601230812473165, 'http': 1.8608112976215943e-06, 'extension': 0.008271078750032843, 'ip': 0.01073912363591437, 'bytes': 56.052936291046251, 'user': 0.0, 'referrer': 0.008818411505907325, 'action': 0.0, 'page': 0.0012894405881835836, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/our-story.php', 'action': 'GET', 'page': '/js/vendor/modernizr-2.6.2.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 171828, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/drylining/', 'action': 'GET', 'page': '/perch/resources/gm-06.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/perch/resources/reynears.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 972, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/js/main.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.css', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 175, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/metal-work.php', 'action': 'GET', 'page': '/css/main.css', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 33691, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/boardroom.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 150, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=66&itm=46', 'action': 'GET', 'page': '/perch/addons/plugins/editors/markitup/images/textile/file.png', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.eot', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 152, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/fonts/fontawesome-webfont.eot?', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.eot', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 2357, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/residential.php', 'action': 'GET', 'page': '/fonts/flexslider-icon.eot?', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 173, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/news/', 'action': 'GET', 'page': '/js/main.js', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 2032, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=25', 'action': 'GET', 'page': '/perch/core/assets/js/templates.js?_=1408091268859', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 173, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=448', 'action': 'GET', 'page': '/perch/core/assets/js/headroom.min.js?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/templates/generic.php', 'action': 'GET', 'page': '/img/50-years-service.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 173, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/js/main.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 152, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/residential.php', 'action': 'GET', 'page': '/perch/resources/edenbrook1.png', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 633, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/', 'action': 'GET', 'page': '/perch/core/inc/js_privs.php?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 149, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/add/?pid=47', 'action': 'GET', 'page': '/perch/core/assets/img/bg@2x.png', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 3139, 'datetime': 0, 'user': '-', 'referrer': '-', 'action': 'GET', 'page': '/', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 5121, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/services/metal-work.php', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00648876345182384, 'ip': 0.01073912363591437, 'bytes': 35.5049790017571, 'user': 0.0, 'referrer': 0.008877889316532649, 'action': 0.0003679575550085889, 'page': 0.0012743823991554573, 'browser': 0.006165279250406871})
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 4860, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/about/our-story.php', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00648876345182384, 'ip': 0.01073912363591437, 'bytes': 38.511190579258674, 'user': 0.0, 'referrer': 0.008877889316532649, 'action': 0.0003679575550085889, 'page': 0.0012747452470838459, 'browser': 0.000626042244871562})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/services.php', 'action': 'GET', 'page': '/img/Customers/Dryvit.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.9, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '66.249.64.184', 'offset': 1, 'bytes': 3891, 'datetime': 0, 'user': '-', 'referrer': '-', 'action': 'GET', 'page': '/portfolio/residential-high-rise/stevenage-homes.php', 'browser': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
(0.9, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.007427632596897634, 'ip': 0.01073912363591437, 'bytes': 43.202596095763042, 'user': 0.0, 'referrer': 0.008377697450787742, 'action': 0.0003679575550085889, 'page': 0.0012992979569048072, 'browser': 0.004822676244399373})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 173, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/metal-work.php', 'action': 'GET', 'page': '/js/main.min.js', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '66.249.64.174', 'offset': 1, 'bytes': 8744, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/education/', 'action': 'GET', 'page': '/js/plugins.min.js', 'browser': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 4780, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/contact.php', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00648876345182384, 'ip': 0.01073912363591437, 'bytes': 39.455196129552355, 'user': 0.0, 'referrer': 0.008877889316532649, 'action': 0.0003679575550085889, 'page': 0.0012768013853447146, 'browser': 0.00614862919070284})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 150, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/metal-work.php', 'action': 'GET', 'page': '/img/Customers/Eos.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '66.249.81.247', 'offset': 1, 'bytes': 275149, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/drylining/', 'action': 'GET', 'page': '/perch/resources/04-7.jpg', 'browser': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko; Google Web Preview) Chrome/27.0.1453 Safari/537.36'}
(0, None)
===========================================
(0.999, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 2100615, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/divisions/drylining-1.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
(0.999, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.0, 'bytes': 105.07442280584446, 'user': 0.0, 'referrer': 0.006855643755271653, 'action': 0.0003679575550085889, 'page': 0.0012966975467513554, 'browser': 0.004426255096912737})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 150, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/perch/resources/aquarian.png', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/why-choose-stanmore.php', 'action': 'GET', 'page': '/js/vendor/modernizr-2.6.2.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '195.162.126.18', 'offset': 1, 'bytes': 1683, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/js/main.js', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/600.3.18 (KHTML, like Gecko) Version/8.0.3 Safari/600.3.18'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 6220, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/KRend.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/js/vendor/modernizr-2.6.2.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 339453, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/tcdesignexterior040-1.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 35.88297709328517, 'user': 0.0, 'referrer': 0.006855643755271653, 'action': 0.0003679575550085889, 'page': 0.0012916176757539152, 'browser': 0.00015782577601804025})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 150, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/customers.php', 'action': 'GET', 'page': '/perch/resources/cpl.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 6660, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Dryvit.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/divisions/fascias-division-w600h400.jpg', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/our-story.php', 'action': 'GET', 'page': '/img/Customers/Knopp.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/our-story.php', 'action': 'GET', 'page': '/perch/resources/event-photo.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 4653, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/services/dry-lining.php', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00648876345182384, 'ip': 0.01073912363591437, 'bytes': 40.97628407280996, 'user': 0.0, 'referrer': 0.006813926679763613, 'action': 0.0003679575550085889, 'page': 0.001273959076572337, 'browser': 0.00614862919070284})
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 81007, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/perch/resources/hadleys.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '66.249.64.174', 'offset': 1, 'bytes': 8744, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/education/', 'action': 'GET', 'page': '/js/plugins.min.js', 'browser': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 28962, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/customers.php', 'action': 'GET', 'page': '/perch/resources/breyergroup.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 2819, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/?id=8', 'action': 'GET', 'page': '/perch/core/apps/content/', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '66.249.67.19', 'offset': 1, 'bytes': 5077, 'datetime': 0, 'user': '-', 'referrer': '-', 'action': 'GET', 'page': '/services/glazing.php', 'browser': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.00648876345182384, 'ip': 0.01073912363591437, 'bytes': 36.004041684898766, 'user': 0.0, 'referrer': 0.006473168389722698, 'action': 0.0003679575550085889, 'page': 0.0012766804360352516, 'browser': 0.00715476851281785})
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '213.205.241.237', 'offset': 1, 'bytes': 264561, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/perch/resources/4.jpg', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 158416, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/perch/resources/3.jpg', 'browser': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 202812, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/drylining/', 'action': 'GET', 'page': '/perch/resources/04-4.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 614, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/edit/?id=47', 'action': 'GET', 'page': '/perch/core/inc/js_lang.php?_=1405459876502', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 31.667958041770241, 'user': 0.0, 'referrer': 0.008865911146337271, 'action': 0.0003679575550085889, 'page': 0.0012922224223012296, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.css', 'ip': '151.227.155.245', 'offset': 1, 'bytes': 175, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/dry-lining.php', 'action': 'GET', 'page': '/css/main.css', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/templates/generic.php', 'action': 'GET', 'page': '/img/Customers/Downer.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0.9, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 3947, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/contact.php', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'}
(0.9, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.007427632596897634, 'ip': 0.01073912363591437, 'bytes': 43.993678957014012, 'user': 0.0, 'referrer': 0.0069717080940613465, 'action': 0.0003679575550085889, 'page': 0.0012941576112526353, 'browser': 0.002015207725225988})
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 614, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/?id=12', 'action': 'GET', 'page': '/perch/core/inc/js_lang.php?_=1405460569948', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 31.667958041770241, 'user': 0.0, 'referrer': 0.008867976348095096, 'action': 0.0003679575550085889, 'page': 0.0012922224223012296, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/js/vendor/modernizr-2.6.2.min.js', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 216567, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/perch/resources/fundermax.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '78.60.174.149', 'offset': 1, 'bytes': 5383, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/img/Customers/Cemex.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 32.595871023730687, 'user': 0.0, 'referrer': 0.008877889316532649, 'action': 0.0003679575550085889, 'page': 0.0012646459797436968, 'browser': 0.000626042244871562})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 153, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/', 'action': 'GET', 'page': '/perch/resources/divisions/drylining-1.jpg', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/health-and-safety/', 'action': 'GET', 'page': '/img/Customers/Alucobond.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/why-choose-stanmore.php', 'action': 'GET', 'page': '/img/Customers/Cemex.gif', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/options/?id=69', 'action': 'GET', 'page': '/perch/addons/plugins/editors/markitup/jquery.markitup.js', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.jpg', 'ip': '213.205.241.237', 'offset': 1, 'bytes': 264561, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/glazing.php', 'action': 'GET', 'page': '/perch/resources/4.jpg', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/templates/home-page.php', 'action': 'GET', 'page': '/img/stanmore-logo.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '195.89.17.82', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/facades.php', 'action': 'GET', 'page': '/img/Customers/Euroform.png', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36'}
(0, None)
===========================================
(0.999, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.png', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 366, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=42', 'action': 'GET', 'page': '/perch/core/assets/img/bg@1x.png', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0.999, {'returncode': 0.0003601230812473165, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 52.672343298485806, 'user': 0.0, 'referrer': 0.008791150842704052, 'action': 0.0003679575550085889, 'page': 0.0012969394453702812, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.28.136', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/our-story.php', 'action': 'GET', 'page': '/img/Customers/Euroclad.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0.999, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 345, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=530', 'action': 'POST', 'page': '/perch/core/apps/assets/upload/', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0.999, {'returncode': 0.0003601230812473165, 'http': 1.8608112976215943e-06, 'extension': 0.008271078750032843, 'ip': 0.01073912363591437, 'bytes': 49.568754046891527, 'user': 0.0, 'referrer': 0.008737042556649071, 'action': 0.0, 'page': 0.0012894405881835836, 'browser': 0.00614862919070284})
===========================================
(0.9, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 3851, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/portfolio/commercial.php', 'action': 'GET', 'page': '/portfolio/education.php', 'browser': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)'}
(0.9, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.007427632596897634, 'ip': 0.01073912363591437, 'bytes': 42.628107797054682, 'user': 0.0, 'referrer': 0.008863845944579448, 'action': 0.0003679575550085889, 'page': 0.001298027989155447, 'browser': 0.006659438385007383})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '151.227.155.245', 'offset': 1, 'bytes': 175, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/services/dry-lining.php', 'action': 'GET', 'page': '/js/plugins.js', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 614, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/page/?id=15', 'action': 'GET', 'page': '/perch/core/inc/js_lang.php?_=1405458909405', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 31.667958041770241, 'user': 0.0, 'referrer': 0.008867976348095096, 'action': 0.0003679575550085889, 'page': 0.0012922224223012296, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 151, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/health-and-safety/', 'action': 'GET', 'page': '/img/50-years-service.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.css', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=530', 'action': 'GET', 'page': '/perch/core/assets/css/assets.css?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
===========================================
(0.8, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.php', 'ip': '151.227.152.48', 'offset': 1, 'bytes': 614, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/options/?id=87', 'action': 'GET', 'page': '/perch/core/inc/js_lang.php?_=1405460519297', 'browser': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36'}
(0.8, {'returncode': 0.014632297747315344, 'http': 1.8608112976215943e-06, 'extension': 0.010004984335258366, 'ip': 0.01073912363591437, 'bytes': 31.667958041770241, 'user': 0.0, 'referrer': 0.008870041549852919, 'action': 0.0003679575550085889, 'page': 0.0012922224223012296, 'browser': 0.006165279250406871})
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.gif', 'ip': '81.105.30.97', 'offset': 1, 'bytes': 6660, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/about/customers.php', 'action': 'GET', 'page': '/perch/resources/dryvit.gif', 'browser': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
(0, None)
===========================================
(0, None)
{'returncode': 200, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '66.249.67.3', 'offset': 1, 'bytes': 1055, 'datetime': 0, 'user': '-', 'referrer': '-', 'action': 'GET', 'page': '/js/main.min.js', 'browser': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
(0, None)
===========================================
(0, None)
{'returncode': 304, 'http': 'HTTP/1.1', 'extension': '.js', 'ip': '81.149.135.148', 'offset': 1, 'bytes': 174, 'datetime': 0, 'user': '-', 'referrer': 'http://stanmore.menczykowski.co.uk/perch/core/apps/content/edit/?id=530', 'action': 'GET', 'page': '/perch/core/assets/js/head.min.js?v=2.7', 'browser': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'}
(0, None)
