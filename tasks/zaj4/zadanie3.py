# -*- coding: utf-8 -*-
import math

import numpy as np


class Integrator(object):

    """
    Klasa która implementuje całki metodą Newtona Cotesa z użyciem interpolacji
    N-tego stopnia :math:`n\in<2, 11>`.

    Dodatkowe wymaganie: Ilość operacji wykonanych w kodzie Pythona nie może zależeć 
    od num_evaluations. Mówiąc potocznie: nie ma "fora".

    UWAGA: Zachęcam do użycia współczynników NC z zajęć numer 2. Można
    je pobrać od innego zespołu!

    Podpowiedź: nasz algorytm działa tak że najpierw dzieli przedział na
    N podprzedziałów a każdy całkuje metodą NC. Wektoryzacja całkowania
    podprzedziału jest prosta:

    >>> coefficients = np.asanyarray(self.PARAMS[7]) # Wspolczynniki NC
    >>> x = ... # Tutaj wyznaczacie wsółrzędne
    >>> res = (x * coefficients) * norma

    A czy da się stworzyć tablicę X tak by dało się policzyć jednym wywołaniem
    całkę dla wszystkich podprzedziałów?

    Podpowiedź II: Może być to trudne do uzyskania jeśli będziecie używać macierzy
    jednowymiarowej. Należy użyć broadcastingu.

    Podpowiedź III: Proszę o kontakt to podpowiem więcej.

    """

    PARAMS = {
        2: [1, 1],
        3: [1, 4, 1],
        4: [1, 3, 3, 1],
        5: [7, 32, 12, 32, 7],
        6: [19, 75, 50, 50, 75, 19],
        7: [41, 216, 27, 272, 27, 216, 41],
        8: [751, 3577, 1323, 2989, 2989, 1323, 3577, 751],
        9: [989, 5888, -928, 10496, -4540, 10496, -928, 5888, 989],
        10: [None] * 10,
        11: [None] * 11
    }

    PARAMS[10][0] = PARAMS[10][-1] = 2857
    PARAMS[10][1] = PARAMS[10][-2] = 15741
    PARAMS[10][2] = PARAMS[10][-3] = 1080
    PARAMS[10][3] = PARAMS[10][-4] = 19344
    PARAMS[10][4] = PARAMS[10][-5] = 5778

    PARAMS[11][0] = PARAMS[11][-1] = 16067
    PARAMS[11][1] = PARAMS[11][-2] = 106300
    PARAMS[11][2] = PARAMS[11][-3] = -48525
    PARAMS[11][3] = PARAMS[11][-4] = 272400
    PARAMS[11][4] = PARAMS[11][-5] = -260550
    PARAMS[11][5] = 427368


    @classmethod
    def get_level_parameters(self, level):
        """

        :param int level: Liczba całkowita większa od jendości.
        :return: Zwraca listę współczynników dla poszczególnych puktów
                 w metodzie NC. Na przykład metoda NC stopnia 2 używa punktów
                 na początku i końcu przedziału i każdy ma współczynnik 1,
                 więc metoda ta zwraca [1, 1]. Dla NC 3 stopnia będzie to
                 [1, 3, 1] itp.
        :rtype: List of integers, damy generator, bo nas stać
        """
        if(level==2):
            self.divisor = 1/2
        if(level==3):
            self.divisor = 1/3
        if(level==4):
            self.divisor = 3/8
        if(level==5):
            self.divisor = 4/90
        if(level==6):
            self.divisor = 5/288
        if(level==7):
            self.divisor = 1/140
        if(level==8):
            self.divisor = 7/17280
        if(level==9):
            self.divisor = 4/14175
        if(level==10):
            self.divisor = 9/89600
        if(level==11):
            self.divisor = 5/299376
        #nie wiem czy trzeba podzielić
        self.divisor /= (level-1)


    def __init__(self, level):
        """
        Funkcja ta inicjalizuje obiekt do działania dla danego stopnia metody NC
        Jeśli obiekt zostanie skonstruowany z parametrem 2 używa metody trapezów.
        :param level: Stopień metody NC
        """
        self.level = level

    def integrate(self, func, func_range, num_evaluations):
        """


        :type self: object
        :param callable func: Funkcja którą całkujemy
        :param tuple[int] func_range: Krotka zawierająca lewą i prawą granicę całkowania
        :param in tnum_evaluations:
        :return:
        """
        #to jest liczba punktów w których wywołujemy funkcję
        num_intervals = math.ceil(num_evaluations/self.level)
        num_evaluations = self.level*math.ceil(num_evaluations/self.level)
        h = (func_range[1] -func_range[0])/num_intervals

        self.get_level_parameters(self.level)

        coeffs = np.asarray(self.PARAMS[self.level])*self.divisor
        baza = np.ones((num_intervals, self.level))
        baza = baza * np.linspace(0., num_intervals-1, num_intervals).reshape(1, num_intervals).T
        baza *= h
        baza += func_range[0]
        X = np.linspace(0., (func_range[1]-func_range[0])/num_intervals, self.level, dtype=np.float32)
        X = baza+X
        Y = func(X)
        int_array = coeffs * Y *h
        return int_array.sum()


if __name__ == "__main__":

    ii = Integrator(level=3)
    #print(ii.integrate(np.sin, (0, 2*np.pi), 1000))
    print(ii.integrate(lambda x: x*x, (0, 1), 100))