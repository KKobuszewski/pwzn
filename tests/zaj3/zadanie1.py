# -*- coding: utf-8 -*-
import unittest
import pathlib


class TestClass(unittest.TestCase):
    TESTED_MODULE = None

    DATA_DIR = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        load_data = cls.TESTED_MODULE.load_data
        cls.exc = None
        try:
            print(pathlib.Path(cls.DATA_DIR, "zaj3", "enwiki-20140903-pages-articles_part_3.xml.csv"))
            cls.data = load_data(
                str(pathlib.Path(cls.DATA_DIR, "zaj3", "enwiki-20140903-pages-articles_part_3.xml.csv")))
            cls.data = list(map(list, cls.data))
        except Exception as e:
            cls.data = None
            cls.exc = e

    def setUp(self):
        super().setUp()
        self.load_data = self.TESTED_MODULE.load_data
        self.sugester = self.TESTED_MODULE.suggester

    def test_load_data(self):
        if self.exc:
            raise ValueError("Błąd przy ładowaniu danych") from self.exc
        self.assertIsNotNone(self.data)

    def test_load_data_2(self):
        self.assertEqual(
            [self.data[0][200000:200010], self.data[1][200000:200010]],
            [[' 1259 7', ' 1259 A', ' 1259 B', ' 1259 C', ' 1259 M', ' 1259 P',
              ' 1259 Q', ' 1259 T', ' 1259 W', ' 1259 a'],
             [1, 1, 1, 1, 1, 3, 1, 2, 1, 4]])

    def test_sugester_1(self):
        self.assertEqual(self.sugester('ąęśłóź', self.data), [])

    def test_sugester_2(self):
        self.assertEqual(self.sugester('pytho', self.data), [('n', 1.0)])

    def test_sugester_3(self):
        res = self.sugester('pyth', self.data)
        for ii, (chr, prob) in enumerate(
                [('o', 0.7794117647058824), ('a', 0.1323529411764706), ('e', 0.07352941176470588),
                 ('i', 0.014705882352941176)]):
            with self.subTest(ii):
                self.assertEqual(res[ii][0], chr)
                self.assertAlmostEqual(res[ii][1], prob, places=3)

    def test_sugester_4(self):
        res = self.sugester('oba', self.data)
        for ii, (chr, prob) in enumerate(self.SUG_4_OUT):
            with self.subTest(ii):
                self.assertEqual(res[ii][0], chr)
                self.assertAlmostEqual(res[ii][1], prob, places=3)

    def test_sugester_5(self):
        res = self.sugester('Oba', self.data)
        for ii, (chr, prob) in enumerate(self.SUG_5_OUT):
            with self.subTest(ii):
                self.assertEqual(res[ii][0], chr)
                self.assertAlmostEqual(res[ii][1], prob, places=3)

    SUG_4_OUT = [('l', 0.38515255694026646),
                 ('b', 0.28787064890416847),
                 ('c', 0.07160507090674688),
                 (' ', 0.06628706489041684),
                 ('r', 0.051192522561237644),
                 ('t', 0.03115599484314568),
                 ('g', 0.01826385904598195),
                 ('n', 0.016813493768801032),
                 ('i', 0.01165663944993554),
                 ('s', 0.011549204984959175),
                 ('m', 0.010743446497636441),
                 ('h', 0.010528577567683713),
                 (',', 0.007896433175762784)]

    SUG_5_OUT = [('m', 0.8760520275439939),
                 ('n', 0.03519510328997705),
                 ('d', 0.03442999234889059)]
