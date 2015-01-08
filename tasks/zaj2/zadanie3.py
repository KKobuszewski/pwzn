# -*- coding: utf-8 -*-

import math


class Integrator(object):

    """
    Klasa która implementuje całki metodą Newtona Cotesa z użyciem interpolacji
    N-tego stopnia :math:`n\in<2, 11>`.

    .. note::

        Używamy wzorów NC nie dlatego że są super przydatne (zresztą gorąco
        zniechęcam Państwa przed pisaniem własnych podstawowych algorytmów
        numerycznych --- zbyt łatwo o głupi błąd) ale dlatego żebyście
        jescze raz napisali jakiś algorytm w którym nie opłaca się zrobić 11
        ifów.

    """

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
        if(level==1):
              coeff_list = [1,1]
              self.divisor = 1/2
        if(level==2):
              coeff_list = [1,4,1]
              self.divisor = 1/3
        if(level==3):
              coeff_list = [1,3,3,1]
              self.divisor = 3/8
        if(level==4):
              coeff_list = [7,32,12,32,7]
              self.divisor = 4/90
        if(level==5):
              coeff_list = [19,75,50,50,75,19]
              self.divisor = 5/288
        if(level==6):
              coeff_list = [41,216,27,272,27,216,41]
              self.divisor = 1/140
        if(level==7):
              coeff_list = [751,3577,1323,2989,2989,1323,3577,751]
              self.divisor = 7/17280
        if(level==8):
              coeff_list = [989,5888,-928,10496,-4540,10496,-928,5888,989]
              self.divisor = 4/14175
        if(level==9):
              coeff_list = [2857,15741,1080,19344,5778,5778,19344,1080,15741,2857]
              self.divisor = 9/89600
        if(level==10):
              coeff_list = [16067,106300,-48525,272400,-269550,427368,-269550,272400,-48525,106300,16067]
              self.divisor = 5/299376
        if(level==11):
              #złe współczynniki - nie moglismy znaleźć
              coeff_list = [16067,106300,-48525,272400,-269550,427368,-269550,272400,-48525,106300,16067]
              self.divisor = 5/299376

        self.divisor /= level
        return (coeff for coeff in coeff_list)
            

    def __init__(self, level):
        """
        Funkcja ta inicjalizuje obiekt do działania dla danego stopnia metody NC
        Jeśli obiekt zostanie skonstruowany z parametrem 2 używa metody trapezów.
        :param level: Stopień metody NC
        """
        self.level = level

    def integrate(self, func, func_range, num_evaluations):
        """
        Funkcja dokonuje całkowania metodą NC.

        :param callable func: Całkowana funkcja, funkcja ta ma jeden argument,
                              i jest wołana w taki sposób: `func(1.0)`.
        :param Tuple[int] func_range: Dwuelementowa krotka zawiera początek i koniec
                                 przedziału całkowania.
        :param int num_evaluations: Przybliżona lość wywołań funkcji ``func``,
            generalnie algorytm jest taki:

            1. Dzielimy zakres na ``num_evaluations/self.level`` przdziałów.
               Jeśli wyrażenie nie dzieli się bez reszty, należy wziąć najmiejszą
               liczbę całkowitą większą od `num_evaluations/self.level``. 
            2. Na każdym uruchamiamy metodę NC stopnia ``self.level``
            3. Wyniki sumujemy.

            W tym algorytmie wykonamy trochę więcej wywołań funkcji niż ``num_evaluations``,
            dokłanie ``num_evaluations`` byłoby wykonywane gdyby keszować wartości
            funkcji na brzegach przedziału całkowania poszczególnych przedziałów.

        :return: Wynik całkowania.
        :rtype: float
        """
        print('CAŁKOWANIE FUNCKJI', func)
        val_integral = 0.								#wartość całki
        len_range = (func_range[1]-func_range[0])						#dlugość przedzialu całkowania
        num_intervals = math.ceil(num_evaluations/self.level)				#ilość podprzedziałow
        len_interval = len_range/num_intervals						#dlugość podprzedziałów
        interval_gen = (func_range[0]+ii*len_interval for ii in range(num_intervals))	#generator zwracający pierwszy punkt kolejnego przedziału
        len_step = len_interval/(self.level)						#odległość pomiędzy sąsiednimi punktami
        
        print('dł. przedziału:\t\t',len_range)
        print('ilość iteracji:\t\t',num_intervals*self.level)
        print('ilość podprzedziałów:\t',num_intervals)
        print('dł. podprzedziału:\t',len_interval)
        print('krok:\t\t\t',len_step,'\n')
        
        #algorytm całkowania
        for begining_interval in interval_gen:
          for ii,coeff in enumerate(self.get_level_parameters(self.level)):
            val_integral += coeff*self.divisor*func(begining_interval+ii*len_step)*len_interval
            #print('x=',begining_interval+ii*len_step,'f(x)=',func(begining_interval+ii*len_step),'delta:',coeff*self.divisor*func(begining_interval+ii*len_step)*len_step)
          #print('wartość całki z podprzedziału:',val_integral)
        
        return val_integral

if __name__ == '__main__':
    i = Integrator(3)
    
    print('Wynik: ',i.integrate(math.sin, (0, 2*math.pi), 30),'\n\n')
    print('Wynik: ',i.integrate(lambda x: x*x, (0, 1), 30),'\n\n')
