# -*- coding: utf-8 -*-

import bisect
import csv
from datetime import datetime

def load_data_gen(path):
    """
    Funkcja która ładuje dane z pliku zawierającego ngramy. Plik ten jest
    plikiem csv zawierającym n-gramy.

    Tak w ogóle tutaj możecie "zaszaleć" i np. nie zwracać list a jakieś
    generatory żeby mniej pamięci zużywać.

    Do testów tej funkcji i tam wynik tej funkcji zostanie potraktowany tak:

    >>> data = load_data('enwiki-20140903-pages-articles_part_0.xmlascii1000.csv')
    >>> data = [list(data[0]), list(data[1])]

    :param str path: Ścieżka
    :return: Lista dwuelementowych krotek, pierwszym elementem jest ngram, drugim
    ilość wystąpień ngramu
    """
    start = datetime.now()
    with open(path, 'r', encoding='utf-8') as file:
        data1 = csv.reader(file, dialect=csv.unix_dialect)
        data2 = csv.reader(file, dialect=csv.unix_dialect)
        return [(row[0] for row in data1), (int(row[1]) for row in data2)]
        print('loading data time:', (datatime.now()-start).total_seconds())
    raise FileNotFoundError

def load_data(path):
    """
    Funkcja która ładuje dane z pliku zawierającego ngramy. Plik ten jest
    plikiem csv zawierającym n-gramy.

    Tak w ogóle tutaj możecie "zaszaleć" i np. nie zwracać list a jakieś
    generatory żeby mniej pamięci zużywać.

    Do testów tej funkcji i tam wynik tej funkcji zostanie potraktowany tak:

    >>> data = load_data('foo')
    >>> data = [list(data[0]), list(data[1])]

    :param str path: Ścieżka
    :return: Lista dwuelementowych krotek, pierwszym elementem jest ngram, drugim
    ilość wystąpień ngramu

    ma byc krotka, list/generatorów
    """
    #import csv

    with open(path, "r", encoding='utf-8') as file:
        data=csv.reader(file, dialect=csv.unix_dialect)
        #for d in data: yield (d[0],int(d[1]))
        ngram=[]
        ilosc_ngram=[]
        for d in data:
            ngram.append(d[0])
            ilosc_ngram.append(int(d[1]))
        return ngram, ilosc_ngram


def suggester(input, data):
    """
    Funkcja która sugeruje następną literę ciągu ``input`` na podstawie n-gramów
    zawartych w ``data``.

    :param str input: Ciąg znaków o długości 6 znaków lub mniejszej
    :param list data: Data jest krotką zawierającą dwie listy, w pierwszej liście
                      zawarte są n-gramy w drugiej ich częstotliwości.
                      Częstotliwość n-gramu data[0][0] jest zawarta w data[0][1]

    :return: Listę która zawiera krotki. Pierwszym elementem krotki jest litera,
             drugim prawdopodobieństwo jej wystąpienia. Lista jest posortowana
             względem prawdopodobieństwa tak że pierwszym elementem listy
             jest krotka z najbardziej prawdopodobną literą.

    Przykład implementacji
    ----------------------

    By wygenerować częstotliwości należy:

    Dla ustalenia uwagi zakładamy ze input zawiera ciąg znaków `foo`

    1. Odnaleźć pierwsze wystąpienie ngramu rozpoczynającego się od wartości
       ``foo``. Tutaj polecam algorytm przeszukiwania binarnego i moduł
       ``bisect``.
    2. Znaleźć ostatnie wystąpienie ngramu. Tutaj można albo ponownie przeszukać 
       binarnie, albo założyć po prostu przeszukać kolejene elementy listy.

       .. note::

            Kroki 1 i 2 można zastąpić mało wydajnym przeszukiwaniem naiwnym,
            tj. przeiterować się po liście i jeśli ciąg znakóœ rozpoczyna się od
            'foo' (patrz: https://docs.python.org/3.4/library/stdtypes.html#str.startswith)
            zapamiętujemy go

    3. Stworzyć słownik który odwzorowuje następną literę (tą po `foo`) na
       ilość wystąpień. Pamiętaj że w data może mieć taką zawartość 
       ``[['fooabcd', 300], ['fooa    ', 300]]`` --- co w takim wypadku w słowniku tym
       powinno być {'a': 600}.

    4. Z tego słownika wyznaczyć prawdopodobieństwo wystąpienia kolejnej litery.

    Przykład zastosowania:

    >>> data = load_data("enwiki-20140903-pages-articles_part_3.xml.csv")
    >>> suggester('ąęćś', data)
    []
    >>> suggester('pytho', data)
    [('n', 1.0)]
    >>> suggester('pyth', data)
    [('o', 0.7794117647058824),
     ('a', 0.1323529411764706),
     ('e', 0.07352941176470588),
     ('i', 0.014705882352941176)]
    """
    min_index = bisect.bisect_left(data[0], input)
    #print(data[0][len(input)+1])
    #print([ii for ii in letter_gen(data, min_index, input)])
    suggests = []
    sugg_index = 0
    sum = 0
    for ii, suggest in enumerate(letter_gen(data, min_index, input)):
        """
        suggest = [str letter, int freq]
        """
        sum += suggest[1]
        if ii == 0:
            suggests.append(suggest)
            last_char = suggest[0]
        elif last_char == suggest[0]:
            suggests[sugg_index][1] += suggest[1]
        else:
            sugg_index += 1
            suggests.append(suggest)
            last_char = suggest[0]
        #print(suggest, suggests)
    suggests = [(suggest[0], suggest[1]/sum) for suggest in suggests] #obliczamy prawdopodobieństwo
    suggests.sort(key=lambda x: -x[1])  #sortujemy wg prawdopodobieństwa
    return suggests


def letter_gen(data, min_index, input):
    """
    generator of ngrams
    :param data:        data to be used
    :param min_index:   index of smalles ngram with string of characters the same as input
    :param input:       string of characters to be compred
    :return:            generator of list of ngrams containing the same string of chars as input (first field)
                        with frequency (second field)
    """
    for ii, ngram in enumerate(data[0][min_index:]):
        if ngram[0:(len(input))] == input:
            yield [ngram[len(input)], data[1][min_index+ii]]
        else:
            break


#data = load_data("enwiki-20140903-pages-articles_part_0.xmlascii1000.csv")
#print(type(data),type(data[0]),type(data[1]))

#print(suggester('pytho', data))
#print(suggester('foo', data))
