# -*- coding: utf-8 -*-


################################################################################
### Kod pomocniczy od prowadzącego
################################################################################

import csv
import io
import os.path
import bz2
import re
import itertools
from xml.dom.pulldom import parse, START_ELEMENT
from collections import defaultdict


link_re = re.compile("\[\[([^\[\]\|]+)(?:\|[^\]]+)?\]\]")


def text_from_node(node):
    """
    Przyjmuje węzeł XML i zwraca kawałki zawartego w nim tekstu
    """
    for ch in node.childNodes:
        if ch.nodeType == node.TEXT_NODE:
            yield ch.data


def clean_page(page_contents):
    """
    Pobiera iterator tekstu i w (z dużymi błędami) usuwa z niego markup Wikipedii
    oraz normalizuje go.

    .. warning::

        Ten lgorytm czyszczenia markupu Wikipedii ma więcej wad niz zalet.
        W zasadzie zaletę ma jedną: nie wymaga instalacji parsera Wikipedii,
        i będzie tak samo działać na Windowsie co na Linuksie.

        Ogólnie jest tu duze pole do poprawy.
    """
    page = io.StringIO()
    for c in page_contents:
        page.write(c)

    page = page.getvalue()

    page = re.sub(r"[^a-zA-Z0-9\.\,\;\s]", " ", page, flags=re.UNICODE)
    page = re.sub("\s+", " ", page, flags=re.UNICODE | re.MULTILINE)

    return page


def iter_over_contents(IN):
    """
    Pobiera nazwę pliku i zwraca iterator który zwraca krotki
    (tytuł strony, wyczyszczona zawartość).

    Działa to na tyle sprytnie że nie ładuje całego XML do pamięci!
    :param IN:
    :return:
    """
    open_func = open
    print(type(IN),IN,str(str(IN).lower()[-3:]))

    if str(IN).lower()[-1:-3] == "bz2":#IN.endswith("bz2"):
        open_func = bz2.open
    with open_func(str(IN)) as f:
        doc = parse(f)
        for event, node in doc:
            if event == START_ELEMENT and node.tagName == 'page':
                doc.expandNode(node)
                text = node.getElementsByTagName('text')[0]
                title = node.getElementsByTagName('title')[0]
                title = "".join(text_from_node(title))
                yield title, clean_page(text_from_node(text))

################################################################################
### Kod pomocniczy od prowadzącego === END
################################################################################


def generate_ngrams(contents, ngram_len=7, default_return=True):
    """
    Funkcja wylicza częstotliwość n-gramów w części wikipedii.
    N-gramy są posortowane względem zawartości n-grama.

    Testiowanie tej funkcji na pełnych danych może być uciążliwe, możecie
    np. po 1000 stron kończyć tą funkcję.

    :param generator contents: Wynik wywołania funkcji: ``iter_over_contents``,
        czyli generator który zwraca krotki: (tytuł, zawartość artykułu).
    :param int ngram_len: Długość generowanych n-gramów. Jeśli parametr ten
        przyjmie wartość 1 to wyznaczacie Państwo rozkład częstotliwości
        pojawiania się poszczególnyh liter w wikipedii

    :return: Funkcja zwraca słownik n-gram -> ilość wystąpień
    """

    ngram_dict=defaultdict(lambda : 0)
    for content in contents:
        text = content[1]# + ' ' + content[0]
        #print(text, len(text))
        for ii, letter in enumerate(text):
            if ii == len(text) - ngram_len + 1:
                break
            ngram = text[ii:ngram_len+ii]
            ngram_dict[ngram] += 1
    if default_return is True:
        return dict(ngram_dict)
    else:
        return ngram_dict


def save_ngrams(out_file, contents):
    """
    Funkcja działa tak jak `generate_ngrams` ale zapisuje wyniki do pliku
    out_file. Może wykorzystywać generate_ngrams!

    Plik ma format csv w dialekcie ``csv.unix_dialect`` i jest posortowany
    względem zawartości n-grama.

    :param dict ngram_dict: Słownik z n-gramami
    :param str out_file: Plik do którego n-gramy zostaną zapisane
    """
    with open(out_file, 'w') as f:
        w = csv.writer(f, dialect=csv.unix_dialect)
        for ngram, freq in generate_ngrams(contents, ngram_len=1).items():
            w.writerow([ngram, freq])


if __name__ == '__main__':
    ngram_dict = generate_ngrams([("foo", "Ala ma kota a Marta ma Asa")], 3)
    por = {'la ': 1, 'Asa': 1, 'ma ': 2, 'Mar': 1, 'a A': 1, 'art': 1, 'Ala': 1, ' ma': 2, ' As': 1, 'a k': 1, 'ta ': 2, 'rta': 1, 'kot': 1, 'a m': 2, ' a ': 1, ' Ma': 1, 'ota': 1, 'a a': 1, ' ko': 1, 'a M': 1}
    #
    counter = 0
    for ngram, p in itertools.zip_longest(sorted(ngram_dict.items(), key=lambda x: x[0]), sorted(por.items(), key=lambda x: x[0])):
        counter += 1
        print('{}.\t'.format(counter),ngram, '\t', p)