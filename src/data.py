
import pandas as pd
import numpy as np
import utils
from datetime import datetime
from utils import DatePart
from datasets.superstore import superstore

## Load SuperstoreSales dataset
DATA = superstore.DATASET

## Declare skeleton
SKELETON = {
    'Row ID': {},
    'Order ID': {},
    'Order Date': {},
    'Order Priority': {},
    'Order Quantity': {},
    'Sales': {},
    'Discount': {},
    'Ship Mode': {},
    'Profit': {},
    'Unit Price': {},
    'Shipping Cost': {},
    'Customer Name': {},
    'Province': {},
    'Region': {},
    'Customer Segment': {},
    'Product Category': {},
    'Product Sub-Category': {},
    'Product Name': {},
    'Product Container': {},
    'Product Base Margin': {},
    'Ship Date': {}
     }

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

## Shuffle it
DATA = DATA.reindex(np.random.permutation(DATA.index))

## Create skeleton from data
for c in DATA:
    # General type and weight
    SKELETON[ c ] = { 'UserWeight': 0.0, 'Type': str(DATA.dtypes[c]), 'DataType': 'None', 'Distance': 'None' }
    SKELETON[ c ]['Info'] = Info( DATA, c )
    # Frequency table
    freq = DATA[ c ].value_counts().to_dict()
    for v in freq:
        freq[v] = float(freq[v]) / float(len(DATA))
    SKELETON[ c ]['FrequencyTable'] = freq

## These values will be given by user
## UserWeight: How important this feature is.
## The sum must be "one"
## If you cannot weight them manually, then give all to equal weights (excluding ones with type none)
SKELETON['Row ID']['UserWeight'] = 0.0
SKELETON['Order ID']['UserWeight'] = 0.0
SKELETON['Order Date']['UserWeight'] = 0.05
SKELETON['Order Priority']['UserWeight'] = 0.05
SKELETON['Order Quantity']['UserWeight'] = 0.05
SKELETON['Sales']['UserWeight'] = 0.05
SKELETON['Discount']['UserWeight'] = 0.05
SKELETON['Ship Mode']['UserWeight'] = 0.05
SKELETON['Profit']['UserWeight'] = 0.05
SKELETON['Unit Price']['UserWeight'] = 0.05
SKELETON['Shipping Cost']['UserWeight'] = 0.05
SKELETON['Customer Name']['UserWeight'] = 0.05
SKELETON['Province']['UserWeight'] = 0.05
SKELETON['Region']['UserWeight'] = 0.05
SKELETON['Customer Segment']['UserWeight'] = 0.05
SKELETON['Product Category']['UserWeight'] = 0.05
SKELETON['Product Sub-Category']['UserWeight'] = 0.05
SKELETON['Product Name']['UserWeight'] = 0.05
SKELETON['Product Container']['UserWeight'] = 0.05
SKELETON['Product Base Margin']['UserWeight'] = 0.00
SKELETON['Ship Date']['UserWeight'] = 0.05

## These values will also be given by user
## These values show which type of values they do have
## Possible acceptable data types are ["None", "Short FreeText", "Categoric", "Date", "DateTime", "Flag", "Ordinal", "Numeric"]
SKELETON['Row ID']['DataType'] = 'None'
SKELETON['Order ID']['DataType'] = 'None'
SKELETON['Order Date']['DataType'] = 'Date'
SKELETON['Order Priority']['DataType'] = 'Ordinal'
SKELETON['Order Quantity']['DataType'] = 'Numeric'
SKELETON['Sales']['DataType'] = 'Numeric'
SKELETON['Discount']['DataType'] = 'Numeric'
SKELETON['Ship Mode']['DataType'] = 'Categoric'
SKELETON['Profit']['DataType'] = 'Numeric'
SKELETON['Unit Price']['DataType'] = 'Numeric'
SKELETON['Shipping Cost']['DataType'] = 'Numeric'
SKELETON['Customer Name']['DataType'] = 'Short FreeText'
SKELETON['Province']['DataType'] = 'Categoric'
SKELETON['Region']['DataType'] = 'Categoric'
SKELETON['Customer Segment']['DataType'] = 'Ordinal'
SKELETON['Product Category']['DataType'] = 'Categoric'
SKELETON['Product Sub-Category']['DataType'] = 'Categoric'
SKELETON['Product Name']['DataType'] = 'Categoric'
SKELETON['Product Container']['DataType'] = 'Categoric'
SKELETON['Product Base Margin']['DataType'] = 'None'
SKELETON['Ship Date']['DataType'] = 'Date'

MIN_DATE = datetime.strptime("1/1/2009", "%m/%d/%Y")
MAX_DATE = datetime.strptime("12/30/2012", "%m/%d/%Y")
SKELETON['Order Date']['bins'] = DatePart.get_date_partitions(MIN_DATE, MAX_DATE, datepart=12)
SKELETON['Order Quantity']['bins'] = utils.listextension([1], range(5, 51, 5)) # 1, 5, 10, 15, ..., 45, 50
SKELETON['Sales']['bins'] = range(0, 90001, 900) # 0, 900, 1800, ..., 89.100, 90.000
SKELETON['Discount']['bins'] = [i * 0.01 for i in range(0, 26, 5)] # 0.00, 0.05, ..., 0.20, 0.25
SKELETON['Profit']['bins'] = range(-30000, 30001, 600)
SKELETON['Unit Price']['bins'] = range(0, 7001, 70)
SKELETON['Shipping Cost']['bins'] = range(0, 201, 5)
SKELETON['Ship Date']['bins'] = DatePart.get_date_partitions(MIN_DATE, MAX_DATE, datepart=12)


## These values will be filled by user
## These values show which metric will be used for distance comparison
SKELETON['Row ID']['Distance'] = 'None'
SKELETON['Order ID']['Distance'] = 'None'
SKELETON['Order Date']['Distance'] = 'd:Date'
SKELETON['Order Priority']['Distance'] = 'a:Ordinal'
SKELETON['Order Quantity']['Distance'] = 'n:MAPE'
SKELETON['Sales']['Distance'] = 'n:MAPE'
SKELETON['Discount']['Distance'] = 'n:MAPE'
SKELETON['Ship Mode']['Distance'] = 's:Categoric'
SKELETON['Profit']['Distance'] = 'n:MAPE'
SKELETON['Unit Price']['Distance'] = 'n:MAPE'
SKELETON['Shipping Cost']['Distance'] = 'n:MAPE'
SKELETON['Customer Name']['Distance'] = 'None'
SKELETON['Province']['Distance'] = 's:Categoric'
SKELETON['Region']['Distance'] = 's:Categoric'
SKELETON['Customer Segment']['Distance'] = 'Ordinal'
SKELETON['Product Category']['Distance'] = 's:Categoric'
SKELETON['Product Sub-Category']['Distance'] = 's:Categoric'
SKELETON['Product Name']['Distance'] = 's:Categoric'
SKELETON['Product Container']['Distance'] = 's:Categoric'
SKELETON['Product Base Margin']['Distance'] = 'None'
SKELETON['Ship Date']['Distance'] = 'd:Date'

## These values will be generated from a function [system assigned weights]
## These values will be calculated by some statistical calculations
SKELETON['Row ID']['Weight'] = 0.0
SKELETON['Order ID']['Weight'] = 0.0
SKELETON['Order Date']['Weight'] = 0.05
SKELETON['Order Priority']['Weight'] = 0.05
SKELETON['Order Quantity']['Weight'] = 0.05
SKELETON['Sales']['Weight'] = 0.05
SKELETON['Discount']['Weight'] = 0.05
SKELETON['Ship Mode']['Weight'] = 0.05
SKELETON['Profit']['Weight'] = 0.05
SKELETON['Unit Price']['Weight'] = 0.05
SKELETON['Shipping Cost']['Weight'] = 0.05
SKELETON['Customer Name']['Weight'] = 0.05
SKELETON['Province']['Weight'] = 0.05
SKELETON['Region']['Weight'] = 0.05
SKELETON['Customer Segment']['Weight'] = 0.05
SKELETON['Product Category']['Weight'] = 0.05
SKELETON['Product Sub-Category']['Weight'] = 0.05
SKELETON['Product Name']['Weight'] = 0.05
SKELETON['Product Container']['Weight'] = 0.05
SKELETON['Product Base Margin']['Weight'] = 0.00
SKELETON['Ship Date']['Weight'] = 0.05
