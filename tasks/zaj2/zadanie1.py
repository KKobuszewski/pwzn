# -*- coding: utf-8 -*-


def xrange(start=0, stop=None, step=None):
    """
    Funkcja która działa jak funkcja range (wbudowana i z poprzednich zajęć)
    która działa dla liczb całkowitych.

    """
    #print(args,stop,step)
    x = start
    if step is None:
        step = 1
    if stop is None:
        stop = start
        x = 0
    while x < stop:
        yield x
        x = x + step

#print(list(xrange(2,15,2)))#przez print nie tworzy sie referencja;
print(list(xrange(5)))





"""
    range(n) creates a list containing all the integers 0..n-1. 
    This is a problem if you do range(1000000), because you'll end up with a >4Mb list. 
    xrange deals with this by returning an object that pretends to be a list,
    but just works out the number needed from the index asked for, and returns that.
    
    
    For performance, especially when you're iterating over a large range, xrange() is usually better. 
    However, there are still a few cases why you might prefer range():
    
    In python 3, range() does what xrange() used to do and xrange() does not exist. 
    If you want to write code that will run on both Python 2 and Python 3, you can't use xrange().
    
    range() can actually be faster in some cases - eg. if iterating over the same sequence multiple times.  
    xrange() has to reconstruct the integer object every time, but range() will have real integer objects.
    (It will always perform worse in terms of memory however)
    
    xrange() isn't usable in all cases where a real list is needed.
    For instance, it doesn't support slices, or any list methods.
    
"""