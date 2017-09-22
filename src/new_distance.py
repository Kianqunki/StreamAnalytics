# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 07:56:33 2017

@author: eyazici
"""

# -*- coding: utf-8 -*-

## Imports ##################################################################################
import re # Regular expressions
from itertools import groupby # Grouping operations
import numpy as np # Numerical operation
import utils
## Internal functions ########################################################################
## __checktype
## Checks the types of variables
## @typename: The name of the type, one letter "n" ...
## @a: The first input to be checked
## @b: The second input to be checked
## @return: True/False indicating type is ok or not
## @completed, @incremental
def __checktype( typename, a, b ):
    # Check that the type of the variable is anything
    if typename == "a":
        return True
    # Check that the type of the variable is string
    if typename == "s":
        return type(a) is str and type(b) is str
    # Check that the type of the variable is "n:Numeric" which accepts int or float
    if typename == "n":
        return (isinstance(a, np.int64) or np.integer(a) or type(a) is int or type(a) is float or type(a) is np.int64) and (type(b) is int or type(b) is float or type(b) is np.int64 or np.integer(b) or isinstance(b, np.int64))
    # For unknown types
    return False

## __longestCommonSubsequence
## Returns the longest common subsequence
## @s1: The first input
## @s2: The second input
## @return: The longest common subsequence
## @completed
def __longestCommonSubsequence(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result

## __longestCommonSubstring
## Returns the longest common substring
## @s1: The first input
## @s2: The second input
## @return: The longest common substring
## @completed
def __longestCommonSubstring( s1, s2 ):
    longest = ""
    i = 0
    for x in s1:
        if re.search(x, s2):
          s = x
          while re.search(s, s2):
            if len(s)>len(longest):
                longest = s
            if i+len(s) == len(s1):
                break
            s = s1[i:i+len(s)+1]
        i += 1
    return longest

## __soundex
## Calculates the soundex
## @word: The input word
## @return: The soundex
## @completed
def __soundex(word):
    word = word.lower()
    codes = ("bfpv","cçgğjkqşsxz", "dt", "l", "mn", "r")
    soundDict = dict((ch, str(ix+1)) for ix,cod in enumerate(codes) for ch in cod)
    cmap2 = lambda kar: soundDict.get(kar, '9')
    sdx =  ''.join(cmap2(kar) for kar in word.lower())
    sdx2 = word[0].upper() + ''.join(k for k,g in list(groupby(sdx))[1:] if k!='9')
    sdx3 = sdx2[0:4].ljust(4,'0')
    return sdx3

## __soundexDistance
## Calculates the soundex distance
## @a: The first input
## @b: The second input
## @return: The soundex distance
## @completed
def __soundexDistance( a, b ):
    wa = __soundex( a )
    wb = __soundex( b )
    if wa[0] != wb[0]:
        return 1.0
    return 1.0 - float(abs(int(wa[1]) - int(wb[1])) * 100 + abs(int(wa[2]) - int(wb[2])) * 10 + abs(int(wa[2]) - int(wb[2]))) / 1000.0

## _jaccard
## Calculates the jaccard distance
## @a: The input 1 string
## @b: The input 2 string
## @return: The ratio of distance
## @completed
def __jaccard( a, b ):
    aw = a.split(' ')
    bw = b.split(' ')

    common = 0.0
    different = 0.0

    for i in aw:
        if i in bw:
            common += 1
        else:
            different += 1

    for i in bw:
        if i in aw:
            common += 1
        else:
            different += 1

    return float(common) / float(different+common)

## __categoric
## Calculates the categoric distance
## @a: The first input
## @b: The second input
## @info: The info
## @return: Returns the categoric distance
## @completed
def __categoric( a, b, info ):
    if a == b:
        return 0.0
    return info["FrequencyTable"][ a ] +  info["FrequencyTable"][ b ]

## __weightedJaccard
## Calculates the jaccard distance
## @a: The input 1 string
## @b: The input 2 string
## @info: The info
## @return: The ratio of distance
## @completed
def __weightedJaccard( a, b, info ):
    aw = a.split(' ')
    bw = b.split(' ')

    common = 0.0
    different = 0.0

    for i in aw:
        if i in bw:
            common += info.getTermValue( i )
        else:
            different += info.getTermValue( i )

    for i in bw:
        if i in aw:
            common += info.getTermValue( i )
        else:
            different += info.getTermValue( i )

    return float(common) / float(different+common)

## __levenshteinDistance
## Calculates the levenshtein distance
## @str1: The input 1 string
## @str2: The input 2 string
## @return: The ratio of distance
## @completed
def __levenshteinDistance(str1, str2):
    m = len(str1)
    n = len(str2)
    lensum = float(m + n)
    d = []
    for i in range(m+1):
        d.append([i])
    del d[0][0]
    for j in range(n+1):
        d[0].append(j)
    for j in range(1,n+1):
        for i in range(1,m+1):
            if str1[i-1] == str2[j-1]:
                d[i].insert(j,d[i-1][j-1])
            else:
                minimum = min(d[i-1][j]+1, d[i][j-1]+1, d[i-1][j-1]+2)
                d[i].insert(j, minimum)
    ldist = d[-1][-1]
    ratio = (lensum - ldist)/lensum
    return ratio #{'distance':ldist, 'ratio':ratio}

## __ip
## Calculates the ip distance
## @a: The input 1 string
## @b: The input 2 string
## @info: The info
## @return: The distance
## @completed
def __ip( a, b ):
    aa = a.split('.')
    bb = b.split('.')
    
    #: If they are
    if a == b:
        return 0.0
    
    #: If the first three parts are not same
    if aa[0:2] != bb[0:2]:
        return 1.0
    
    #: Return
    return 0.5

## Shortcut functions ########################################################################
## fabs
## Float abs
## @input: The input
## @return: Floated absolute value
## @completed
def fabs( input ):
    return float(abs(input))

## Main Functions ###########################################################################
## __distance
## Calculates the distance
## @a: The first input
## @b: The second input
## @info: The information
## @datatype: The type of the column
## @on_both_none: Value if both none
## @on_none: Value if one of them is none
## @return: Distance [0-1]
## @completed
def __distance( a, b, info, datatype, on_both_none = 0.0, on_none = 1.0 ):
    # Check the type name exists in database
    assert datatype in utils.DISTANCE_TYPES
    # Check nulls
    if a == None and b == None:
        return on_both_none
    if a == None or b == None:
        return on_none

    # Evaluate for each type of value
    if datatype == "a:Hamming":
        return 0.0 if a == b else 1.0
    elif datatype == "s:Levenshtein":
        return 1.0 - __levenshteinDistance( a, b )
    elif datatype == "s:Longest Common Substring":
        return 1.0 - float(len(__longestCommonSubstring( a, b ))) / float(max(len(a), len(b)))
    elif datatype == "s:Longest Common Subsequence":
        return 1.0 - float(len(__longestCommonSubsequence( a, b ))) / float(max(len(a), len(b)))
    elif datatype == "s:Jaccard":
        return 1.0 - __jaccard( a, b )
    elif datatype == "s:Weighted Jaccard":
        return 1.0 - __weightedJaccard( a, b, info['Info'] )
    elif datatype == "s:Categoric":
        return 1.0 - __categoric( a, b, info )
    elif datatype == "s:Soundex":
        return 1.0 - __soundexDistance( a, b )
    elif datatype == "n:MAPE":
        return abs(float(abs((a - b))) / float(a+b+0.00001)) * 2.0
    elif datatype == "n:Normalized MAPE":
        return ((float(abs((a - b))) / float(a+b)) * info['Info'].getStandardDeviation())
    elif datatype == "s:IP":
        return __ip( a, b )

    # Should not reach here
    print "Error: Not defined distance data type " + datatype
    # Default value
    return -1.0

## distance
## Calculates the distance between two rows
## @a: Row 1
## @b: Row 2
## @SKELETON: The skeleton
## @on_both_none: On Both none
## @on_none: On Both none
## @return: The weighted cummulative distance
## @completed, incremental
def mixeddistance( a, b, SKELETON, on_both_none = 0.0, on_none = 1.0, withDesc = False ):
   
    # Declare
    dist = 0.0
    desc = {}
    # Each
    for c in SKELETON:
        if SKELETON[c]["Distance"] == "None":
            dist = dist + 0.0
        elif not SKELETON[c]["Distance"] in utils.DISTANCE_TYPES:
            print "ERROR NOT IMPLEMENTED DATA TYPE:" + SKELETON[c]["Distance"]
            dist = dist + 0.0 # TO DO
        else:
            weight = SKELETON[c]["UserWeight"] * SKELETON[c]["Weight"]
            dd = __distance( a[c], b[c], SKELETON[c], SKELETON[c]["Distance"], on_both_none, on_none ) * weight
            desc[ c ] = dd
            dist = dist + dd
    
    # Return
    if withDesc == True:
        return desc
    else:
        return dist
