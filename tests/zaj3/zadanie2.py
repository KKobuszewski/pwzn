# -*- coding: utf-8 -*-
import csv
import unittest
import pathlib
import os
import tempfile
import hashlib


def load_data(path):
    """
    # WARN: Tak to jest rozwiązanie poprzedniego zadania!
    """
    keys = []
    frequencies = []

    with open(path, encoding='utf-8') as f:
        wr = csv.reader(f, dialect=csv.unix_dialect)
        for row in wr:
            keys.append(row[0])
            frequencies.append(int(row[1]))

    return keys, frequencies


class TestClass(unittest.TestCase):

    TESTED_MODULE = None

    DATA_DIR = None

    result = []

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if not cls.SHORT:
            merge = cls.TESTED_MODULE.merge
            file1 = str(pathlib.Path(cls.DATA_DIR, "zaj3", "enwiki-20140903-pages-articles_part_0.xmlascii1000.csv"))
            file2 = str(pathlib.Path(cls.DATA_DIR, "zaj3", "enwiki-20140903-pages-articles_part_1.xmlascii1000.csv"))
            cls.out = tempfile.mktemp()
            cls.exc = None
            cls.result = None
            try:
                merge(file1, file2, cls.out)
                cls.result = load_data(cls.out)
            except Exception as e:
                cls.result = None
                cls.exc = e

    def setUp(self):
        super().setUp()
        self.merge = self.TESTED_MODULE.merge

    def test_load_data(self):
        if self.SHORT:
            self.fail("By uzyskać ocenę odpal pełne testy")
        if self.exc:
            raise ValueError("Błąd przy ładowaniu danych") from self.exc
        self.assertIsNotNone(self.result)

    def short_test(self, list1, list2, list3):

        i1 = tempfile.mktemp()
        i2 = tempfile.mktemp()
        o = tempfile.mktemp()

        try:
            with open(i1, 'w') as f:
                w = csv.writer(f, dialect=csv.unix_dialect)
                w.writerows(list1)

            with open(i2, 'w') as f:
                w = csv.writer(f, dialect=csv.unix_dialect)
                w.writerows(list2)

            self.merge(i1, i2, o)

            with open(o) as f:
                r = csv.reader(f, dialect=csv.unix_dialect)
                self.assertEqual([[i[0], int(i[1])] for i in r], list3)
        finally:
            os.remove(i1)
            os.remove(i2)
            os.remove(o)


    def test1(self):
        self.short_test([['a', 1], ['b', 2]], [], [['a', 1], ['b', 2]])

    def test2(self):
        self.short_test([], [['a', 1], ['b', 2]], [['a', 1], ['b', 2]])

    def test3(self):
        self.short_test([['a', 1], ['b', 2]], [['a', 1], ['b', 2]], [['a', 2], ['b', 4]])

    def test4(self):
        self.short_test(
            [['a', 1], ['b', 2], ['d', 4]],
            [['a', 1], ['c', 3]],
            [['a', 2], ['b', 2], ['c', 3], ['d', 4]]
        )

    def test_merged(self):
        if not self.SHORT:
            self.assertEqual(len(self.result[0]), 6631370)

    def test_merged_beginning(self):
        if not self.SHORT:
            self.assertEqual(
                [self.result[0][:10], self.result[1][:10]],
                [[' , , , ', ' , , . ', ' , , ..', ' , , .j', ' , , 0 ', ' , , 1 ', ' , , 10', ' , , 19', ' , , 20', ' , , 38'], [45, 11, 1, 1, 2, 1, 1, 2, 3, 1]]
            )

    def test_merged_end(self):
        if not self.SHORT:
            print(self.result[0][-30:])
            self.assertEqual(
                [self.result[0][-10:], self.result[1][-10:]],
                [['zzy and', 'zzy blo', 'zzy log', 'zzy sys', 'zzy yes', 'zzy, Mi', 'zzy, ps', 'zzy9QC ', 'zzyMemo', 'zzymemo'], [3, 1, 7, 2, 1, 1, 1, 1, 2, 1]]
            )

    def test_sha(self):
        if not self.SHORT:
            with open(self.out, 'rb') as f:
                sha = hashlib.sha256()
                for l in f:
                    sha.update(l)
                self.assertEqual(
                    sha.hexdigest(), '4960a12403a49132e13a990adf848d9170c025b2a7a6d196601d6d04ac952559',
                    "Skrót SHA-256 Waszego pliku jest niepoprawny. Jego zawartość jest nieodpowiednia :)")
