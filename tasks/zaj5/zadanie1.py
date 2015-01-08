# -*- coding: utf-8 -*-
from numpy import char

import numpy as np

def next_item(input):
    """
    Zwraca "następny" ngram dla podanego n-gramu. Działa to dla ciągów znaków ASCII.
    To jest hak, ale działa.

    Można zaimplementować to lepiej.
    :param input:
    :return:
    """
    return input[:-1] + chr(ord(input[-1])+1)


def load_data(path):
    """
    Funkcja która ładuje dane z pliku zawierającego ngramy. Plik ten jest
    plikiem binarnym zaiweającym N wieszy w każdym wierszu jest 7 bajtów 
    zawierających 7-gram a następie czterobajtowa liczba całkowita zawierającą 
    ilość zlieczeń.

    Funkcja zwraca tablicę numpy. Tablica ja jest tylko do odczytu.

    Podpowiedźź: starczą dwie linikji kodu definicja dtype oraz otwarcie macierzy.
    Typ danych jest złożony --- należy użyć Structured Array.
    """
    dtype = np.dtype([('ngram', np.dtype("a7")), ('frequencies', np.uint32)])
    data = np.memmap(path, dtype=dtype)
    return data


def suggester(input, data):
    """
    Funkcja która sugeruje następną literę ciągu ``input`` na podstawie n-gramów
    zawartych w ``data``.

    :param str input: Ciąg znaków o długości 6 znaków. **UWAGA** W zajęciach trzecich
                      input mógł mieć dowolną długość.
    :param np.ndarray data: Wynik działania ``load_data``.
    :return: Dowolną strukturę którą można zaindeksować w następującyc sposób:
            ret[0][0] zwraca najbardziej prawdopodobną nasßępną literę. ret[0][1]
            jej prawdopodobieństwo. ret[-1][0] zwraca najmniej prawdopodobną literę.
            Dane posortowane są względem prawodpodobieństwa.

    By wygenerować częstotliwości należy:

    Dla ustalenia uwagi zakładamy ze input zawiera ciąg znaków `foo`

    1. Znaleźć "następny" n-gram. Krótka funkcja "hak", która zwraca następny
       n-gram jest z
    2. Odnaleźć pierwsze i ostatnie wystąpienie ngramu rozpoczynającego się od wartości
       ``foo``.
    3. Wyznaczyć prawdopodobieństwo wystąpienia kolejnej litery, posortować i zwrócić.

    Przykład zastosowania:

    >>> data = load_data("path")
    >>> suggester('ąęćś', data)
    []
    >>> suggester('pytho', data)
    [('n', 1.0)]
    >>> suggester('pytho', data)
    [('o', 0.7794117647058824),
     ('a', 0.1323529411764706),
     ('e', 0.07352941176470588),
     ('i', 0.014705882352941176)]
    """
    index_left = np.searchsorted(data['ngram'], np.asanyarray([input]))
    index_right = np.searchsorted(data['ngram'], np.asanyarray([next_item(input)]))
    #print(index_left, index_right, data[index_left:index_right])

    #suggests = [(chr(d[0][-1]), d[1]) for d in data[index_left:index_right]]
    #print(data[index_left:index_right])
    sum_freqs = np.sum(data[index_left:index_right]['frequencies'])
    #print('sum', sum_freqs)
    suggests = [(chr(d[0][-1]), int(d[1])/int(sum_freqs)) for d in data[index_left:index_right]]

    suggests.sort(key=lambda x: (-x[1], x[0]))

    print(suggests)
    #test się krzaczy, gdyż dane nie są posortowane wg prawdopodobieństwa i kolejności alfabetycznej
    # tylko wg prawdopodobienstwa
    return suggests


if __name__ == '__main__':
    suggester('integr',load_data('/home/konrad/Pulpit/pwzn_bzdak/tasks/zaj5/enwiki-20140903-pages-articles_part_1.xmlascii1000.bin'))