import resolve_modules
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from anomaly_score import AnomalyScore
from utils import DatePart
from datetime import datetime, timedelta

# Generate bins for numeric data
bins = [x * 0.02 for x in range(-100, 100)]
start_date = datetime.strptime("1/1/2017", "%m/%d/%Y") 
end_date = start_date + timedelta(days=365)
date_bins = DatePart.get_date_partitions(start_date, end_date, datepart=12)
dates = [start_date + timedelta(days = np.random.randint(0, 365)) for i in range(1000)]

# Create skeleton as dataset metadata
skeleton = {
    "a":{
        "DataType":"Numeric", 
        "bins":bins}, 
    "b":{
        "DataType":"Numeric", 
        "bins":bins},
    "c":{
        "DataType":"Categoric"},
    "dates":{
        "DataType":"Date", 
        "bins":date_bins
    }}

# Generate dataset
X_train = pd.DataFrame(np.random.randn(1000,2), columns=["a","b"])
X_train["c"] = ["Cat" + str(i/100) for i in range(1000)]
X_train["dates"] = dates

# Generate test instances
date1 = datetime.strptime("10/12/2017", "%m/%d/%Y") 
date2 = datetime.strptime("6/27/2017", "%m/%d/%Y") 
X_test = pd.DataFrame({"a":[-1.97, -1], "b":[1.98, 1], "c":["Cat3", "Cat4"], "dates":[date1, date2]})

# calculate anomaly score distributions and print scores and bins for feature 'a' 
anomaly = AnomalyScore(skeleton)
anomaly.fit(X_train)
print "Distributions: ", anomaly.distributions["a"][0][:5]
print "Bins: ", anomaly.distributions["a"][1][:5]
print "\n"
print "Distributions: ", anomaly.distributions["dates"][0]
print "Bins: ", anomaly.distributions["dates"][1]

# find anomaly scores for every instance feature in test dataset
predictions = anomaly.predict(X_test)
print predictions
