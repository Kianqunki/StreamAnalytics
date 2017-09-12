# Impors
from pymongo import MongoClient

# The streaming works on two modes.
# First mode is the learning mode.
# Second mode is the assignin mode.
MODE = 1

# Stack is a temporary list of storing the samples until they are enough to be learnt
STACK = []

# A list of created clusters, it stores information of clusters
CLUSTERS = []
# uniq: The uniq name of the cluster
# size: The size of the cluster
# size%: The size of the cluster in percentage 
# avg.d: Average distance between samples
# max.d: Maximum distance between samples
# .....:

# Mongo Db connection
DBCLIENT = MongoClient( 'localhost', 27017 ) # mongo port
DATABASE = DBCLIENT[ 'mongo-db' ]

## __necessary_samples
## Returns the necessary samples for the system to learn, then it can start assigning
## @return: The number of samples
## @completed
def __necessary_samples():
    return 30 * 30 # TODO: Make it static right now but normally, it will be [cols] x [cols]

## Main function
## stream
## Process the incoming row/record
## @incoming: The incoming row
## @completed
def stream( incoming ): 
    if MODE == 1:
        STACK.push( incoming )
        if len(STACK) > __necessary_samples():
            __analyze_initial_samples()
            MODE = 2
            STACK = []
    elif MODE == 2:
        __assign( incoming )

## __assign
## Assigns the incoming row to appropriate cluster
## @incoming: The incoming row
## @completed
def __assign( incoming ):
    # Declare variables
    distance = 10000.0
    c = -1
    
    # Loop for each items to find the closest cluster
    for i in range(len(CLUSTERS)):
        d = __find_distance_cluster( CLUSTER[i], incoming )
        if d < distance:
            distance = d
            c = i
    
    # Insert the record and its belonging cluster to database [mongo]
    some = incoming
    some['cluster'] = CLUSTER[c].uniq
    DATABASE[ 'logtable' ].insert( some )
    
    # Update the c[th] cluster according to the incoming 
    if len(CLUSTER[c].INTERNAL_STACK) > 100 # TODO: CHANGE THIS
        __update_cluster( c, incoming )
        CLUSTER[c].INTERNAL_STACK = []
    else:
        CLUSTER[c].INTERNAL_STACK.append( incoming )

# __find_distance_cluster
# Find the distance between a row and a cluster
# @cluster: The input cluster
# @incoming: The incoming row
# @return: The distance
# @completed
def __find_distance_cluster( cluster, incoming ):
    # TODO: Normally, the distance should be calculated also on mahalanobis distance
    # It will depend on the variation of the cluster (size/dimension/diameter)
    return distance( cluster.avgrw, incoming, SKELETON )





def __update_cluster( cluster_index, incoming):
    # THIS FUNCTION UPDATES THE CLUSTERS
    # NOT COMPLETED
    pass

def __analyze_initial_samples():
    pass


#
