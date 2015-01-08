__author__ = 'karolina'
import pyximport; pyximport.install()
from qsort3 import quicksort#!!!!!!!!serio?
from time import time

import numpy as np

list=np.random.rand(1000)
start=time()
quicksort(list,0,999)
print(time()-start)
