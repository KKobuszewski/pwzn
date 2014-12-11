__author__ = 'konrad'

import csv
import math
import itertools
import time

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
    t = time.time()
    with open(out_file, 'w', encoding='utf-8') as outfile:
        writer = csv.writer(outfile, dialect=csv.unix_dialect)
        # print(itertools.islice(data2, None), type(itertools.islice(data2, None)))

        #stop_loop = False
        buffer = [None, None]
        #iteracja = 0
        while True:
            #iteracja += 1
            #print('{}. iteracja'.format(iteracja), buffer)
            #czytamy generatory data1, data2, musimy sprawdzić każdy z nich czy nie skończył im się plik do czytania
            try:
                d1 = next(data1)
            except StopIteration:
                #jeżeli skończył się plik data1 to dopisujemy same data2
                try:
                    d2 = next(data2)
                except StopIteration:
                    #jeżeli podniósł się ten wyjątek to oba pliki się skończyły
                    break
                else:
                    if (buffer[0] is not None) and (buffer[0] < d2[0]):
                        #print('skończył się data1, zapisano', buffer)
                        writer.writerow(buffer)
                        buffer = [None]
                    elif (buffer[0] is not None) and (buffer[0] > d2[0]):
                        pass
                    elif (buffer[0] is not None) and (buffer[0] == d2[0]):
                        d2[1] += buffer[1]
                        buffer = [None]
                    #print('skończył się data1, zapisano', d2)
                    writer.writerow(d2)
            else:
                try:
                    d2 = next(data2)
                except StopIteration:
                    #jeżeli skończył się plik data2 to dopisujemy same data1
                    if (buffer[0] is not None) and (buffer[0] < d1[0]):
                        #print('skończył się data1, zapisano', buffer)
                        writer.writerow(buffer)
                        buffer = [None]
                    elif (buffer[0] is not None) and (buffer[0] > d1[0]):
                        pass
                    elif (buffer[0] is not None) and (buffer[0] == d1[0]):
                        d1[1] += buffer[1]
                        buffer = [None]
                    #print('skończył się data1, zapisano', d1)
                    writer.writerow(d1)
                else:
                    if buffer[1] is None:
                        if d1[0] == d2[0]:
                            d1[1] += d2[1]
                            #print('zapisano', d1)
                            writer.writerow(d1)
                            buffer = [None, None]
                        elif d1[0] < d2[0]:
                            #print('zapisano', d1)
                            writer.writerow(d1)
                            buffer = d2
                        else:
                            #print('zapisano', d2)
                            writer.writerow(d2)
                            buffer = d1
                    else:
                        triple = sorted([buffer, d1, d2], key=lambda x: x[0])
                        #print(triple)
                        if triple[0][0] != triple[1][0]:
                            if triple[1][0] == triple[2][0]:
                                triple[1][1] += triple[2][1]
                                buffer = [None, None]
                            else:
                                buffer = triple[2]
                            #print('zapisano:', triple[0], triple[1])
                            writer.writerow(triple[0])
                            writer.writerow(triple[1])
                        else:
                            if triple[0][0] == triple[1][0]:
                                triple[0][1] += triple[1][1]
                                buffer = triple[2]
                            if triple[0][0] == triple[2][0]:
                                triple[0][1] += triple[2][1]
                                buffer = [None, None]
                            #print(triple[0])
                            writer.writerow(triple[0])
            #print('bufor:', buffer)


if __name__ == '__main__':

    #merge(#'enwiki-20140903-pages-articles_part_0.xmlascii1000.csv',
    #      #'enwiki-20140903-pages-articles_part_2.xmlascii1000.csv',
    #      #'Merge2.csv')
    #      #'test1.csv', 'test2.csv', 'Test.csv')
    #      'merge1.csv', 'merge3.csv', 'merge.csv')
    merge("enwiki-20140903-pages-articles_part_0.xmlascii1000.csv","enwiki-20140903-pages-articles_part_3.xml.csv","out.csv")