import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.utils import Directory

aa = sys.path

directory = Directory.current().moveup()
datastore = "".join([str(directory), "/SuperstoreSales.xls"])

superstore = pd.read_excel(datastore)
# sns.countplot(y="Order Date", data=superstore, color="b")
# plt.show()
orderdates = superstore["Order Date"]
orderdates = orderdates.astype("string").astype("datetime64")
orderdates.groupby([orderdates.dt.year, [int(i / 3) + int(i % 3 > 0) for i in orderdates.dt.month]]).count().plot(kind="line")
plt.show()