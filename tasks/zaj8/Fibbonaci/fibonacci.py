__author__ = 'konrad'

import pyximport
pyximport.install()
from time import time
from fib import fib


def pfib(n):
    if n < 2:
        return 1
    return fib(n-1) + fib(n-2)

start = time()
print(fib(35))
print('czas:', time()-start)
start = time()
print(pfib(35))
print('czas:', time()-start)

