#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import unittest
import tempfile
from abvdget import Downloader


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


if __name__ == '__main__':
    unittest.main()

