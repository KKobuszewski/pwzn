# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np


def linear_func(x, a, b):
    """
    Funkcja ta zwraca wyznacza a*x + b, funkcja ta powinna działać bez względu
    na to czy x to tablica numpy czy liczba zmiennoprzecinkowa.

    Podpowiedź: Nie jest to bardzo trudne.

    :param np.ndarray x:
    :param float a:
    :param float b:
    """
    return a*x+b


def chisquared(xy, a=1, b=0):
    """

    Funkcja liczy sumę Chi^2 między wartościami zmierzonej funkcji a funkcją 
    liniową o wzorze a*x + b.

    Sumę chi^2 definiujemy jako:

    Chi^2 = Sum(( (y - f(x))/sigma_y)^2)

    gdzie f(x) to w naszym przypadku funkcja liniowa


    :param np.ndarray xy: Tablica o rozmiarze N x 3, w pierwszej kolumnie
        zawarte są wartości zmiennej a w drugiej wartości y.
    :param float a:
    :param float b:
    :return:
    """
    print(xy.shape)
    #print(linear_func(xy[0], a, b) - linear_func(xy[0], a, b))
    return np.sum(((xy[:, 1] - linear_func(xy[:, 0], a, b))/xy[:, 2])**2)


def least_sq(xy):
    """
    Funkcja liczy parametry funkcji liniowej ax+b do danych za pomocą metody
    najmniejszych kwadratów.

    A = (Sum(x^2)*Sum(y)-Sum(x)*Sum(xy))/Delta
    B = (N*Sum(xy)-Sum(x)*Sum(y))/Delta
    Delta = N*Sum(x^2) - (Sum(x)^2)

    :param xy: Jak w chisquared, uwaga: sigma_y nie jest potrzebne.
    :return: Krotka
    """
    XX = np.sum(xy[:, 0]*xy[:, 0])
    X = np.sum(xy[:, 0])
    XY = np.sum(xy[:, 0]*xy[:, 1])
    YY = np.sum(xy[:, 1]*xy[:, 1])
    Y = np.sum(xy[:, 1])
    N = xy.shape[0]
    #print(xy.shape, N)
    Delta = N*np.sum(XX) - np.sum(X)**2
    A = np.sum((XX*Y - X*XY)/Delta)
    B = np.sum((N*XY - X*Y)/Delta)

    return A, B

if __name__ == '__main__':
    print(linear_func(1, 2, 0))
    print(np.linspace(0, 10, 10))
    print(linear_func(np.linspace(0, 10, 10), 5*np.ones((10,), dtype=np.float32), np.zeros((10,), dtype=np.float32)))
    print(linear_func(np.linspace(0, 10, 10), 5, 1))