import resolve_modules
import numpy as np
import pandas as pd
from utils import DatePart
from datetime import datetime

X = pd.DataFrame(np.ones(shape=(10,1)), columns=["a"])
dates = ["1/1/2017","1/2/2017","2/1/2017","3/1/2017","3/1/2017","3/1/2017","6/1/2017","6/2/2017","9/2/2017","10/3/2017"]

dts = []

for i in dates:
    dts.append(datetime.strptime(i, "%m/%d/%Y"))
X["date"] = dts

min_dt = min(dts)
max_dt = max(dts)

print DatePart.get_date_partitions(min_dt, max_dt, datepart=DatePart.Months)
print DatePart.get_date_partitions(min_dt, max_dt, datepart=4)
