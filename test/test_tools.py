#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import unittest

from abvdget.tools import clean, slugify


class TestClean(unittest.TestCase):
    def test_none(self):
        self.assertEqual(clean(None), '')
        
    def test_newline(self):
        self.assertEqual(clean("la\nng"), 'lang')
        
    def test_tab(self):
        self.assertEqual(clean("la\tng"), 'lang')


class Test_Slugify(unittest.TestCase):
    def test_brackets(self):
        self.assertEqual(slugify('Banggai (W.dialect)'), 'Banggai_Wdialect')

    def test_square_brackets(self):
        self.assertEqual(slugify('Buru [Namrole Bay]'), 'Buru')

    def test_dash(self):
        self.assertEqual(slugify('Aklanon - Bisayan'), 'Aklanon_Bisayan')

    def test_accents(self):
        self.assertEqual(slugify('Gimán'), 'Giman')
        self.assertEqual(slugify('Hanunóo'), 'Hanunoo')

    def test_colon(self):
        self.assertEqual(slugify('Kakiduge:n Ilongot'), 'Kakidugen_Ilongot')

    def test_slash(self):
        self.assertEqual(slugify('Angkola / Mandailin'), 'Angkola')
    
    def test_apostrophe(self):
        self.assertEqual(slugify('V’ënen Taut'), 'Venen_Taut')
        
    def test_B(self):
        self.assertEqual(slugify('ßatarobu'), 'Vatarobu')
    
    def test_ng(self):
        self.assertEqual(slugify("Siŋorakai"), "Singorakai")
    
    def test_capital_NG(self):
        self.assertEqual(slugify("Bawah Ŋgusumbatu"), "Bawah_Nggusumbatu")

    def test_j(self):
        self.assertEqual(slugify('xʝalasu'), 'Xjalasu')
        self.assertEqual(slugify('ʝalasu'), 'Jalasu')
    
    def test_e(self):
        self.assertEqual(slugify('Moaekɛ'), 'Moaeke')
    
    def test_palatal_nasal(self):
        self.assertEqual(slugify('Ɲua'), 'Njua')
    
    def test_another_apostrophe(self):
        self.assertEqual(slugify('‘Aragur'), 'Aragur')
