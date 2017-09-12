import pandas as pd
from src.utils import Directory

DATASET = None

def one_time_initialize():
    global DATASET
    if DATASET == None:
        DATASET = pd.read_excel("".join([str(Directory.current()), "/SuperstoreSales.xls"]))
    return DATASET

DATASET = one_time_initialize()
