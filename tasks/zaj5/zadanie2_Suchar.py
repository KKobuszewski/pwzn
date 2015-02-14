# -*- coding: utf-8 -*-

import struct
import mmap
import os
import numpy as np
from time import monotonic as time

__author__ = 'konrad'

class InvalidFormatError(IOError):
    pass

def load_data(filename):
    """
    Funkcja ładuje dane z pliku binarnego. Plik ma następującą strukturę:
    * Nagłówek
    * Następnie struktury z danymi
    Nagłówek ma następującą strukturę:
    0. 16 "magicznych" bajtów te bajty to b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn'
    1. 2 bajty wersji "głównej"
    2. 2 bajty wersji "pomniejszej"
    3. 2 bajty określające rozmiar pojedyńczej struktury danych
    4. 4 bajty określających ilość struktur
    5. 4 bajty określających offset między początkiem pliku a danymi
    6. Następnie mamy tyle struktur ile jest określone w nagłówku
    Struktura danych ma taką postać:
    * event_id: uint16 numer zdarzenia
    * particle_position: 3*float32 we współrzędnych kartezjańskich [m]
    * particle mass: float32 współrzędne kartezjańskie [kg]
    * particle_velocity: 3*float32 współrzędne kartezjańskie [m/s]
    Struktura i nagłówek nie mają paddingu i są zapisani little-endian!
    Ten format pliku jest kompatybilny wstecznie i do przodu w ramach wersji
    "pomniejszej". W następujący sposób:
    * Jeśli potrzebuję dodać jakieś nowe pola do nagłówka to je dodaję,
    i odpowiednio modyfikuję offset między początkiem pliku a danymi.
    Program czytający te pliki który nie jest przystosowany do pracy ze
    starszą wersją może te pola zignorować.
    * Jeśli chce dodać jakieś pola do struktury z danymi to zwiększam pole rozmiar
    jednej struktury danych i dodaje pola. Dane są dodawane do końca struktury,
    więc program czytający dane będzie wiedział że następna struktura zaczyna
    się np. 82 bajty od początku poprzedniej.
    Funkcja ta musi zgłosić wyjątek InvalidLoadError w następujących przypadkach:
    * W pliku nie zgadzają się magiczne bajty
    * Główna wersja pliku nie równa się 3
    * Rozmiar pliku jest nieodpowiedni. Tj rozmiar pliku nie wynosi:
    "offset między początkiem pliku a danymi" + "ilość struktur" * "rozmiar pojedyńczej struktury danych"
    Rada:
    * Proszę załadować nagłówek za pomocą modułu ``struct`` odczytać go,
    a następnie załadować resztę pliku (offset! za pomocą ``np.memmap``).
    Funkcja zwraca zawartość pliku w dowolnym formacie. Testy tego zadania będą
    sprawdzać czy funkcja zgłasza błędy dla niepoprawnych plików.
    W zadaniu 3 będziecie na tym pliku robić obliczenia.
    """

    with open(filename, 'rb') as f:
        s = struct.Struct("<16s3H2I")
        stat = os.stat(filename)
        print(stat)
        if stat.st_size < 30:
            raise InvalidFormatError
        try:
            data = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
            us = s.unpack(data[0 : s.size])
        except:
            raise InvalidFormatError
        if us[0] != b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn':
            raise InvalidFormatError
        if us[1] != 3:
            raise InvalidFormatError
        if data.size() != us[5]+us[4]*us[3]:
            raise InvalidFormatError
        if us[3] < 30:
            raise InvalidFormatError
    dt = [('event_id', np.uint16),
        ('position', np.dtype("3float32")),
        ('mass', np.float32),
        ('velocity', np.dtype("3float32"))]
    if us[3] > 30:
        dt += [('padding', str(us[3]-30)+'a')]
    dtype = np.dtype(dt)
    return np.memmap(filename, dtype=dtype, mode='r', offset=us[5])

if __name__ == '__main__':
    #to nie działa
    data = load_data('zadA')
    #print(data)

    #data2 = load_data('zadB')
    print('\n ZAD A')
    #print(data['event_id'])
    #print(data['position'])
    #print(data['velocity'])
    #print(data['mass'])

    start = time()
    data1 = load_data('zadB')
    print('czas ładowania zadB', time()-start)
    print('\n ZAD B')
    #print(data1['event_id'])
    #print(data1['position'])
    #print(data1['velocity'])
    #print(data1['mass'])