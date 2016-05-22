#!/usr/bin/env python3
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import os
import codecs
import unittest
from xml.dom import minidom

from abvdget import Parser

TESTDATA = os.path.join(os.path.dirname(__file__), 'nengone.xml')

LEX = {
    'annotation': '',
    'pmpcognacy': '',
    'cognacy': '',
    'word': '',
    'id': '',
    'loan': '',
    'word_id': '',
    'item': ''
}
LNG = {
    'notes': None,
    'typedby': 'Penny Keenan',
    'classification': 'Austronesian, Malayo-Polynesian, Central-Eastern Malayo-Polynesian, Eastern Malayo-Polynesian, Oceanic, Central-Eastern Oceanic, Remote Oceanic, Loyalty Islands',
    'checkedby': 'Simon Greenhill',
    'problems': None,
    'silcode': 'nen',
    'author': 'Blust',
    'language': 'Nengone',
    'id': '99'
}

XML_DUPLICATE_LANGUAGE = """
<record>
	<id>99</id>
	<language>Nengone</language>
	<author>Blust</author>
	<silcode>nen</silcode>
	<notes></notes>
	<problems></problems>
	<classification></classification>
	<typedby>Penny Keenan</typedby>
	<checkedby>Simon Greenhill</checkedby>
</record>

<record>
	<id>99</id>
	<language>Nengone</language>
	<author>Blust</author>
	<silcode>nen</silcode>
	<notes></notes>
	<problems></problems>
	<classification></classification>
	<typedby>Penny Keenan</typedby>
	<checkedby>Simon Greenhill</checkedby>
</record>

<record>
	<id>93340</id>
	<word_id>4</word_id>
	<word>leg/foot</word>
	<item>iñtërnâtiônàlizætiøn</item>
	<annotation></annotation>
	<loan></loan>
	<cognacy>13</cognacy>
	<pmpcognacy></pmpcognacy>
</record>

"""

XML_UNKNOWN_RECORD = """
<record>
	<id>99</id>
	<language>Nengone</language>
	<author>Blust</author>
	<silcode>nen</silcode>
	<notes></notes>
	<problems></problems>
	<classification></classification>
	<typedby>Penny Keenan</typedby>
	<checkedby>Simon Greenhill</checkedby>
</record>

<record>
	<id>93340</id>
	<word_id>4</word_id>
	<word>leg/foot</word>
	<item>iñtërnâtiônàlizætiøn</item>
	<annotation></annotation>
	<loan></loan>
	<cognacy>13</cognacy>
	<pmpcognacy></pmpcognacy>
</record>

<record>
    <something>y</something>
</record>
"""

XML_NO_LANGUAGE = """
<record>
	<id>93340</id>
	<word_id>4</word_id>
	<word>leg/foot</word>
	<item>iñtërnâtiônàlizætiøn</item>
	<annotation></annotation>
	<loan></loan>
	<cognacy>13</cognacy>
	<pmpcognacy></pmpcognacy>
</record>
"""

XML_NO_LEXICON = """
<record>
	<id>99</id>
	<language>Nengone</language>
	<author>Blust</author>
	<silcode>nen</silcode>
	<notes></notes>
	<problems></problems>
	<classification></classification>
	<typedby>Penny Keenan</typedby>
	<checkedby>Simon Greenhill</checkedby>
</record>
"""


class Test_Parser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with codecs.open(TESTDATA, 'r') as handle:
            content = handle.read()
        cls.result = Parser().parse(content)
    
    def test_is_lexicon(self):
        self.assertTrue(Parser().is_lexicon(LEX))
        self.assertFalse(Parser().is_lexicon(LNG))
        
    def test_is_language(self):
        self.assertTrue(Parser().is_language(LNG))
        self.assertFalse(Parser().is_language(LEX))
    
    def test_parse_language(self):
        for k in LNG:
            self.assertEqual(LNG[k], self.result['language'][k])
    
    def test_lexicon_count(self):
        self.assertEqual(len(self.result['lexicon']), 4)
    
    def test_lexicon_1(self):
        lex = self.result['lexicon'][0]
        assert lex['id'] == '99'
        assert lex['word'] == 'hand'
        assert lex['item'] == 'nin'
        assert lex['annotation'] == 'arm and hand'
        assert lex['cognacy'] == '1'
    
    def test_empty_cells_are_none(self):
        lex = self.result['lexicon'][0]
        assert lex['id'] == '99'
        assert lex['loan'] is None
    
    def test_utf8(self):
        expected = "iñtërnâtiônàlizætiøn"
        lex = self.result['lexicon'][1]
        assert lex['item'] == expected
    
    def test_duplicate_language(self):
        with self.assertRaises(ValueError):
            Parser().parse(XML_DUPLICATE_LANGUAGE)
        
    def test_unknown_object_type(self):
        with self.assertRaises(ValueError):
            Parser().parse(XML_UNKNOWN_RECORD)

    def test_no_language(self):
        with self.assertRaises(ValueError):
            Parser().parse(XML_NO_LANGUAGE)

    def test_no_lexicon(self):
        with self.assertRaises(ValueError):
            Parser().parse(XML_NO_LEXICON)
    

if __name__ == '__main__':
    unittest.main()

