__author__ = 'konrad'

import csv


def load_data_gen(path):
    """
    loads data as generator
    """
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.reader(f, dialect=csv.unix_dialect)
        # print(type(r))
        for line in r:
            yield [line[0], int(line[1])]


def load_data_list(path):
    """
    :param path:
    :return:
    """
    with open(path, 'r', encoding='utf-8') as f:
        r = csv.reader(f, dialect=csv.unix_dialect)
        return [[line[0], int(line[1])] for line in r]


def merge(path1, path2, out_file):
    """
    Funkcja pobiera nazwy dwóch plików z n-gramami (takie jak w poprzedmim
    zadaniu) i łączy zawartość tych plików i zapisuje do pliku w ścieżce ``out``.

    Pliki z n-gramami są posortowane względem zawartości n-grama.

    :param str path1: Ścieżka do pierwszego pliku
    :param str path2: Ścieżka do drugiego pliku
    :param str out_file:  Ścieżka wynikowa

    Testowanie tej funkcji na pełnych danych może być mało wygodne, możecie
    stworzyć inną funkcję która działa na dwóch listach/generatorach i testować
    ją.

    Naiwna implementacja polegałaby na stworzeniu dwóch słowników które
    zawierają mapowanie ngram -> ilość wystąpień i połączeniu ich.

    Lepsza implementacja ładuje jeden z plików do pamięci RAM (jako słownik
    bądź listę) a po drugim iteruje.

    Najlepsza implementacja nie wymaga ma złożoność pamięciową ``O(1)``.
    Podpowiedź: merge sort. Nie jest to trywialne zadanie, ale jest do zrobienia.
"""
    data1 = load_data_gen(path1)
    data2 = load_data_gen(path2)
    with open(out_file, 'w', encoding='utf-8') as output:
        writer = csv.writer(output, dialect=csv.unix_dialect)
        buffer = [None, None]#zbuforowane elementy
        while True:
            #Sprawdzamy czy pierwszy element jest None
            if buffer[0] is None:
                try:
                    #Jeżeli pierwszy strumień się skończył wyrzuca wyjątek
                    buffer[0] = next(data1)
                except StopIteration:
                    #jeśli trzeba opróżniamy bufor
                    if buffer[1] is not None:
                        writer.writerow(buffer[1])
                    #Wypisujemy cały plik który się nie skończył
                    for d in data2:
                        writer.writerow(d)
                    return
            #Sprawdzamy czy drugi element jest None
            if buffer[1] is None:
                try:
                    buffer[1] = next(data2)
                except StopIteration:
                    #jeśli trzeba opróżniamy bufor
                    if buffer[0] is not None:
                        writer.writerow(buffer[0])
                    #Wypisujemy cały plik który się nie skończył
                    for d in data1:
                        writer.writerow(d)
                    return
            #gdy oba elementy nie są już None
            #sprawdzamy kolejność tak by były posortowane
            if buffer[0][0] > buffer[1][0]:
                buffer = sorted(buffer)
                data1, data2 = data2, data1
            #Jak już są posortowane to sprawdzamy czy nie są równe
            if buffer[0][0] == buffer[1][0]:
                #dodajemy częstotliwości
                writer.writerow([buffer[0][0], int(buffer[0][1]) + int(buffer[1][1])])
                buffer = [None, None]
            #Jeśli nie są równe
            else:
                writer.writerow(buffer[0])
                buffer[0] = None
            """
            #Fajniejsze rozwiązanie
            it = iter(hmerge(data1, data2))
            current = next(it)
            while True:
                try:
                    nxt = next(it)
                    if current[0] == nxt[0]:
                        current[1] = int(current[1]) + nxt[1]
                        nxt = current
                    else:
                        writer.writerow(current)
                        current = nxt
                except StopIteration:
                    writer.writerow(nxt)
                    break
        """
    # Rozwiązanie JBzdak

#def merge(path1, path2, out_file):
"""
    Moja implementacja łączenia. Jest średnio elegancja jeśli chodzi o kod,
    ale dość wydajna. Ta funkcja otwiera pliki i odpala merge_internal.

    """
"""
    with open(path1) as f1, open(path2) as f2, open(out_file, 'w') as o:
        i1 = csv.reader(f1, dialect=csv.unix_dialect)
        i2 = csv.reader(f2, dialect=csv.unix_dialect)
        out = csv.writer(o, dialect=csv.unix_dialect)

        for r in merge_internal(i1, i2):
            out.writerow(r)"""

def merge_internal(i1, i2):
    """

    Moja implementacja łączenia. Jest średnio elegancja jeśli chodzi o kod,
    ale dość wydajna.

    r1 i r2 to właśnie łączone n-gramy.

    Algorytm jest taki:

    * Jeśli aktualnie pobrane obu plików ngramy są sobie równe to zwracamy sumę
      częstotliwości i pobieramy dwa kolejne elementy.
    * Jeśli nie są równe to zwracamy mniejszy i pobieramy nowy element
      na jego miejsce. Możemy zwrócić mniejszy element ponieważ wiemy że
      w drugim pliku nie ma już takiego samego n-gramu.

    """
    pass
"""
    r1, r2 = None, None # "Aktualne" elementy

    while True:
        if r1 is None: # Jeśli r1 nie jest Nonem to pobieramy następny ngram
            try:
                r1 = next(i1)
            except StopIteration:
                if r2 is not None: # r1 się skońvzyło wyrzucamy r2 i resztę elementów z i2
                    yield r2
                for r in i2:
                    yield r
                return
        if r2 is None:  # Jeśli r2 nie jest Nonem to pobieramy następny ngram
            try:
                r2 = next(i2)
            except StopIteration:
                if r1 is not None: # r2 się skońvzyło wyrzucamy r1 i resztę elementów z i1
                    yield r1
                for r in i1:
                    yield r
                return

        # Teraz mamy załadowane zarówno r1 jak i r2

        if r1[0] > r2[0]: # Inwariant jest taki że w r1 zawsze jest mniejszy ngram od r2
            r1, r2 = r2, r1 # Tutaj zamieniamy miejscami zarówno r jak i i
            i1, i2 = i2, i1

        if r1[0] == r2[0]: # Ngramy są sobie równe zwracamy sumę i ustawiamy oba na None (żeby oba się pobrały)
            yield [r1[0], int(r1[1]) + int(r2[1])]
            r1, r2 = None, None
        else: # Jeśli nie są równe zwracamy mniejszy i ustawiamy go na None.
            yield [r1[0], r1[1]]
            r1 = None
    """

if __name__ == '__main__':

    merge(#'enwiki-20140903-pages-articles_part_0.xmlascii1000.csv',
    #      #'enwiki-20140903-pages-articles_part_2.xmlascii1000.csv',
    #      #'Merge2.csv')
    #      #'test1.csv', 'test2.csv', 'Test.csv')
          'merge1.csv', 'merge3.csv', 'merge.csv')
    #merge("enwiki-20140903-pages-articles_part_0.xmlascii1000.csv", "enwiki-20140903-pages-articles_part_3.xml.csv", "out.csv")