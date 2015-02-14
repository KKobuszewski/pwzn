# -*- coding: utf-8 -*-
import numpy as np

from tasks.zaj5.zadanie2 import load_data # Musi tu być żeby testy przeszły


__author__ = 'konrad'

def get_event_count(data):
    """
    Dane w pliku losowane są z takiego rozkładu:
    position, velocity: każda składowa losowana z rozkładu równomiernego 0-1
    mass: losowana z rozkładu równomiernego od 1 do 100.
    Zwraca ilość zdarzeń w pliku. Każda struktura ma przypisane do którego
    wydarzenia należy. Jeśli w pliku jest wydarzenie N > 0
    to jest i wydarzenie N-1.
    :param np.ndarray data: Wynik działania zadanie2.load_data
    """
    return np.max(data['event_id'])

def get_center_of_mass(event_id, data):
    """
    Zwraca macierz numpy zawierajacą położenie x, y i z środka masy układu.
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :return: Macierz 3 x 1
    """
    dane = data[data['event_id'] == event_id]
    #by pomnożyć dane trzeba dopisać do masy nową oś, by mogła się zbroadcastować na 3 wymiary przestrzenne
    #potem sumujemy po pierwszej osi
    return np.sum(dane['mass'][:, np.newaxis]*dane['position'], axis=0)/np.sum(dane['mass'])

def get_energy_spectrum(event_id, data, left, right, bins):
    """
    Zwraca wartości histogramu energii kinetycznej cząstek (tak: (m*v^2)/2).
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :param int left: Lewa granica histogramowania
    :param int right: Prawa granica historamowania
    :param int bins: ilość binów w historamie
    :return: macierz o rozmiarze 1 x bins
    Podpowiedż: np.histogram
    """
    return count_energy_histogram(event_id, data, left, right, bins)[0]

def count_energy_histogram(event_id, data, left, right, bins):
    """\
    :param int event_id: Wybiera tylko te wyniki co mają zadane id
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :param int left: Lewa granica histogramowania
    :param int right: Prawa granica historamowania
    :param int bins: ilość binów w historamie
    :return: macierz o rozmiarze 1 x bins
    """
    data = data[data['event_id'] == event_id]
    #linalg -> linear algebra, liczy normę wektora
    #normę wektora liczymy po 3 współrzędnych przestrzennych -> axis=1
    energy = (1/2)*data['mass']*np.linalg.norm(data['velocity'], axis=1)**2
    return np.histogram(energy, bins=bins, range=(left, right))

if __name__ == "__main__":
    #tutaj pokażemy histogram, bo inaczej to bez sęsu jest
    import matplotlib.pyplot as plt
    data = load_data("zadB")
    print(data['velocity'])
    print(get_event_count(data))
    print(get_center_of_mass(get_event_count(data), data))
    hist, bin_edges = count_energy_histogram(get_event_count(data), data, 0, 90, 100)
    plt.bar(bin_edges[:-1], hist, width = 1)
    plt.xlim(min(bin_edges), max(bin_edges))
    plt.show()
