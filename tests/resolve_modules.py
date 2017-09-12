''' Adds directory of modules into the system path '''
import pandas as pd
import numpy as np
from os import sys
from dir_utils import Directory

MODULE_PATHS = []

MODULE_PATHS.append(Directory.current().moveup().enter("src").path)

for module_path in MODULE_PATHS:
    sys.path.append(module_path)
