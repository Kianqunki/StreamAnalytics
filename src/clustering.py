from sklearn.cluster import DBSCAN
import numpy as np
import simulator as sm
import matplotlib.pyplot as plt
from utils import COLOR_PALETTE

# anomaly = sm.generate_anomaly(-5.0, 5.0, 1000, 0.01)
# noise = sm.generate_noise(0, 0.3, 1000, anomaly)
# noise = np.random.normal(0, 0.3, 1000)

# anomaly = sm.generate_anomaly(-5.0, 5.0, 1000, p_max=0.02, seed=97)
# noise = sm.generate_noise(0, 0.3, 1000, seed=79, anomaly=anomaly)

# values = sm.sinusoid(10, 5, 1000, noise)
# X = np.array([(x,y) for x,y in enumerate(values)])

# dbs = DBSCAN(eps=2, min_samples=2, metric='euclidean')
# labels = dbs.fit_predict(X)

# sizes = [20 if label >= 0 else 100 for label in labels]
# colors = [COLOR_PALETTE[label] 
#           if label < len(COLOR_PALETTE) else COLOR_PALETTE[-1] 
#           for label in labels]

# plt.figure(figsize=(15,10))
# plt.scatter(X[:,0], X[:,1], c=colors, s=sizes)
# plt.plot(X[:,0], X[:,1], c="y", linewidth=5.0, alpha=0.3)
# plt.show()




X = sm.two_moons()

dbs = DBSCAN(eps=0.25, min_samples=12, metric='euclidean').fit(X)
labels = dbs.labels_

colors = [COLOR_PALETTE[label] 
          if label < len(COLOR_PALETTE) else COLOR_PALETTE[-1] 
          for label in labels]

plt.figure(figsize=(15,10))
plt.scatter(X[:,0], X[:,1], c=colors, s=25)
# plt.plot(X[:,0], X[:,1], c="y", linewidth=5.0, alpha=0.3)
plt.show()



