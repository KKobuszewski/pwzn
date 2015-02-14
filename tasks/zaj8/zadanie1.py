__author__ = 'konrad'
import pyximport; pyximport.install()
from Quicksort.original_qsort import quicksort as qsortpy
from qsort import quicksort
from time import monotonic as time

import numpy as np

list1 = np.random.rand(1000)
list2 = np.random.rand(1000)
start = time()
qsortpy(list1, 0, 999)
sec_py = (time()-start)
start2=time()
quicksort(list2, 0, 999)
sec_cyth = (time()-start2)
print('funkcja w czystym pythonie:\t', sec_py, 's')
print('funkcja w cythonie:\t\t\t', sec_cyth, 's')
print('uzyskane przyspieszenie:\t', sec_py/sec_cyth, 'razy')
