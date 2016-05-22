#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import unittest

from abvdget.abvd_download import parse_args as abvd_download_parse_args


class TestABVDDownload_ParseArgs(unittest.TestCase):
    def test_two(self):
        self.assertEqual(
            abvd_download_parse_args(['austronesian', '10']),
            ('austronesian', 10, None)
        )
        
    def test_three(self):
        self.assertEqual(
            abvd_download_parse_args(['austronesian', '10', '-o', 'out.json']),
            ('austronesian', 10, 'out.json')
        )
        
    def test_invalid_database(self):
        with self.assertRaises(SystemExit) as e:
            abvd_download_parse_args(['wals', '10'])
            
    def test_invalid_language_id(self):
        with self.assertRaises(SystemExit) as e:
            abvd_download_parse_args(['austronesian', 'maori'])
    