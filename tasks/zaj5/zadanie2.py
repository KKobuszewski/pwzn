# -*- coding: utf-8 -*-

import mmap
import struct
import numpy as np
from time import monotonic as time

class InvalidFormatError(IOError):
    pass

class InvalidVersionError(InvalidFormatError):
    pass

#class Invalid

def load_data(filename):

    """
    :param file path to be loaded
    :return numpy.ndarray with data
    Funkcja ładuje dane z pliku binarnego. Plik ma następującą strukturę:

    * Nagłówek
    * Następnie struktury z danymi

    Nagłówek ma następującą strukturę:

    0. 16 "magicznych" bajtów te bajty to b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn' -> '16s'
    1. 2 bajty wersji "głównej" -> '2s'
    2. 2 bajty wersji "pomniejszej" -> '2s'
    3. 2 bajty określające rozmiar pojedyńczej struktury danych -> '2s'
    4. 4 bajty określających ilość struktur -> Integer 'I'
    5. 4 bajty określających offset między początkiem pliku a danymi -> Integer 'I'
    6. Następnie mamy tyle struktur ile jest określone w nagłówku

    Struktura danych ma taką postać:

    * event_id: uint16 numer zdarzenia
    * particle_position: 3*float32 we współrzędnych kartezjańskich [m]
    * particle mass: float32 współrzędne kartezjańskie [kg]
    * particle_velocity: 3*float32 współrzędne kartezjańskie [m/s]

    Struktura i nagłówek nie mają paddingu i są zapisane little-endian!

    Ten format pliku jest kompatybilny wstecznie i do przodu w ramach wersji
    "pomniejszej". W następujący sposób:

    * Jeśli potrzebuję dodać jakieś nowe pola do nagłówka to je dodaję,
      i odpowiednio modyfikuję offset między początkiem pliku a danymi.
      Program czytający te pliki który nie jest przystosowany do pracy ze
      starszą wersją może te pola zignorować.
    * Jeśli chce dodać jakieś pola do struktury z danymi to zwiększam pole rozmiar
      jednej struktury danych i dodaje pola. Dane są dodawane do końca struktury,
      więc program czytający dane będzie wiedział że następna struktura zaczyna
      się np. 82 bajty od początku poprzedniej.

    Funkcja ta musi zgłosić wyjątek InvalidLoadError w następujących przypadkach:

    * W pliku nie zgadzają się magiczne bajty
    * Główna wersja pliku nie równa się 3
    * Rozmiar pliku jest nieodpowiedni. Tj rozmiar pliku nie wynosi:
      "offset między początkiem pliku a danymi" + "ilość struktur" * "rozmiar pojedyńczej struktury danych"


    Rada:

    * Proszę załadować nagłówek za pomocą modułu ``struct``  odczytać go,
      a następnie załadować resztę pliku (offset! za pomocą ``np.memmap``).

    Funkcja zwraca zawartość pliku w dowolnym formacie. Testy tego zadania będą
    sprawdzać czy funkcja zgłasza błędy dla niepoprawnych plików.

    W zadaniu 3 będziecie na tym pliku robić obliczenia.
    """
    with open(filename, 'rb') as file:
        #little-endian '<'
        s = struct.Struct("<16sH2s2sII")
        try:
            head = mmap.mmap(file.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
            headline = s.unpack(head[:s.size])
        except Exception:
            raise InvalidFormatError

        #odczytywanie nagłówka
        magic_bytes = headline[0]
        main_version = headline[1]
        subversion = headline[2]
        structure_size = int.from_bytes(headline[3], byteorder='little')
        structures_num = headline[4]
        offset = headline[5]
        #print('file:', filename, '\tsize:', structure_size, ',number of structures:', structures_num, ',offset:', offset)
        if magic_bytes != b'6o\xfdo\xe2\xa4C\x90\x98\xb2t!\xbeurn':
            print('wrong magic spell!')
            raise InvalidFormatError
        if main_version != 3:
            print('wrong version!', main_version)
            raise InvalidVersionError
        if structures_num == 0:
            print('nothing to read!')
            raise InvalidFormatError
        if structures_num*structure_size + offset != head.size():
            print('every headline lies!', structures_num*structure_size + offset, head.size())
            raise InvalidFormatError

        #deklaracja struktury danych
        dtype = np.dtype([
            ('event_id', np.uint16),
            ('position', np.dtype("3float32")),
            ('mass', np.float32),
            ('velocity', np.dtype("3float32")),
            ('padding', np.dtype('{}a'.format(structure_size - 30)))
            ])
        data = np.memmap(filename, mode='r', dtype=dtype, offset=offset, shape=(structures_num,), order='C')
        return data
    raise InvalidFormatError

if __name__ == '__main__':
    #to nie działa
    data = load_data('zadA')
    #print('\n ZAD A')
    #print(data['event_id'])
    #print(data['position'])
    #print(data['velocity'])
    #print(data['mass'])
    #print('padding', data['padding'])

    start = time()
    data1 = load_data('zadB')
    print('\nczas ładowania zadB', time()-start)
    print('\n ZAD B')
    #print(data1['event_id'])
    #print(data1['position'])
    #print(data1['velocity'])
    #print(data1['mass'])
    #print('padding', data['padding'])