# -*- coding: utf-8 -*-

from .zadanie2 import load_data  # Musi tu być żeby testy przeszły
import numpy as np


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
    #print('wynik działania funkcji get_event_count:', np.argmax(data['event_id']))
    print('max index:', data['event_id'])
    index = np.argmax(data['event_id'])
    print('max index:', index)
    print('max event value:', data['event_id'][index])
    return data['event_id'][index]


def get_center_of_mass(event_id, data):
    """
    Zwraca macierz numpy zawierajacą położenie x, y i z środka masy układu.
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :return: Macierz 3 x 1

    ??? PO CO MI EVENT_ID ???
    PRZECIEŻ NIE BĘDĘ ROBIŁ TEGO W FORZE!?

    """
    x = np.dot(data['mass'], data['point'][:, 0]) / np.sum(data['mass'])
    y = np.dot(data['mass'], data['point'][:, 1]) / np.sum(data['mass'])
    z = np.dot(data['mass'], data['point'][:, 2]) / np.sum(data['mass'])
    print('środek masy:', x, y, z)
    print(np.asanyarray([x, y, z], dtype=np.float32, order='C'))
    print(np.asanyarray([x, y, z], dtype=np.float32, order='C').shape)
    return np.asanyarray([x, y, z], dtype=np.float32, order='C')


def get_energy_spectrum(event_id, data, left=0, right=100, bins=10):
    """
    Zwraca wartości histogramu energii kinetycznej cząstek (tak: (m*v^2)/2).
    :param np.ndarray data: Wynik działania zadanie2.load_data
    :param int left: Lewa granica histogramowania
    :param int right: Prawa granica historamowania
    :param int bins: ilość binów w historamie
    :return: macierz o rozmiarze 1 x bins

    Podpowiedż: np.histogram
    """

    energies = np.asanyarray(data['velocity'][:, 0] * data['velocity'][:, 0], dtype=np.float64, order='C')
    energies += np.asanyarray(data['velocity'][:, 1] * data['velocity'][:, 1], dtype=np.float64, order='C')
    energies += np.asanyarray(data['velocity'][:, 2] * data['velocity'][:, 2], dtype=np.float64, order='C')
    energies *= data['mass']
    energies /= 2
    print(energies.shape)
    print(energies[0], data['velocity'][0], data['mass'][0])
    values, bin_edges = np.histogram(energies, bins=bins, range=(left, right))
    print(values.shape)
    return values


if __name__ == "__main__":
    data = load_data("...")
    # print(data['velocity'])
    print(get_event_count(data))
    print(get_center_of_mass(1, data))
    # noinspection PyTypeChecker
    print(list(get_energy_spectrum(3, data, 0, 90, 100)))