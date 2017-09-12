import numpy as np
from sklearn.datasets import make_moons 

def sinusoid(frequency, magnitude, size, noise=None):
    ''' returns array of sinusoidal values '''
    if noise is None:
        noise = np.zeros(size, dtype=float)
    samples = np.arange(0, size)
    return magnitude * np.sin(2 * np.pi * frequency * samples / size) + noise

def two_moons(n_samples=1000, noise=0.05, random_state=None):
    X, label = make_moons(n_samples=n_samples, noise=noise, random_state=random_state)
    return X

def generate_noise(avg, sdev, size, seed=None, anomaly=None):
    ''' Generates noise data

    Args:
        avg     (float) : mean of distribution
        sdev    (float) : standard deviation of distribution
        size    (int)   : size of the sample
        anomaly (array) : array of values representing anomaly

    Returns:
        Array of values representing a noise
    '''
    rnd = np.random.RandomState(seed)
    if anomaly is None:
        anomaly = np.zeros(size, dtype=float)
    return rnd.normal(avg, sdev, size) + anomaly


def generate_anomaly(min, max, size, p=0.0, p_max=1, seed=None):
    rnd = np.random.RandomState(seed)
    if not seed is None:
        p = rnd.uniform(0, p_max)
    anomalies = rnd.choice([0, 1], size, p=[1-p, p])
    anomaly_magnitude = rnd.uniform(min, max, size)
    return anomalies * anomaly_magnitude

# import matplotlib.pyplot as plt
# values = sinusoid(10, 5, 1000, generate_noise(0, 0.3, 1000, generate_anomaly(-5.0, 5.0, 1000, 0.01)))
# plt.plot(values)
# plt.show()
