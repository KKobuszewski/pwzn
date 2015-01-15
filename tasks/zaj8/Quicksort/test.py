__author__ = 'konrad'
import pyximport; pyximport.install()
from original_qsort import quicksort as qsortpy
from qsort import quicksort#!!!!!!!!serio?
from time import monotonic as time

import numpy as np

list=np.random.rand(1000)
start=time()
qsortpy(list, 0, 999)
print(time()-start)
start2=time()
quicksort(list, 0, 999)
print(time()-start2)
