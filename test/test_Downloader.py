#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import unittest
from abvdget import Downloader, DeadLanguageError, InvalidLanguageError


class Test_Downloader(unittest.TestCase):
    def test_error_on_invalid_database(self):
        with self.assertRaises(ValueError):
            Downloader('uralic')
    
    def test_make_url_error_on_noniteger(self):
        with self.assertRaises(TypeError):
            Downloader('bantu').make_url('A')
    
    def test_make_url(self):
        url = Downloader('bantu').make_url('999')
        assert url.endswith('999')
        assert 'bantu' in url
    
    def test_is_valid_language(self):
        d = Downloader('austronesian')
        with self.assertRaises(InvalidLanguageError):
            d.is_valid_language("A")
        with self.assertRaises(InvalidLanguageError):
            d.is_valid_language("Maori")
        with self.assertRaises(DeadLanguageError):
            d.is_valid_language(261)
        # but 261 is only invalid in austronesian
        assert Downloader("bantu").is_valid_language(261)
