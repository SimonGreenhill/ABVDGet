#!/usr/bin/env python3
#coding=utf-8

import json
import codecs
import unicodedata
from xml.dom import minidom
from functools import lru_cache
from collections import namedtuple

import requests

from .CognateParser import CognateParser
from .tools import slugify, clean


XMLTEMPLATE = """
<?xml version="1.0" encoding="utf-8"?>
<abvd>
    %s
</abvd>
""".lstrip().rstrip()


DATABASES = [
    'austronesian',
    'bantu',
    'mayan',
    'utoaztecan',
]

Record = namedtuple("Record", [
    'LID', 'ID', 'WID', 'Language', 'Word', 'Item', 'Annotation', 'Cognacy', 'Loan'
])



class Downloader(object):
    url = "http://language.psy.auckland.ac.nz/utils/save/?type=xml&section=%(db)s&language=%(id)d"
    
    databases = DATABASES
    
    def __init__(self, database):
        if database not in self.databases:
            raise ValueError("Unknown Database: %s" % database)
        self.database = database
        self.data = None
    
    def make_url(self, language_id):
        try:
            language_id = int(language_id)
        except:
            raise TypeError("language_id needs to be an integer")
        
        return self.url % {'db': self.database, 'id': language_id}
    
    @lru_cache(maxsize=2000)
    def get(self, language_id):
        req = requests.get(self.make_url(language_id))
        
        # fail on no content
        if len(req.content) == 0:
            return None
            
        self.data = Parser().parse(req.content.decode('utf8'))
        return self.data
    
    def write(self, filename):
        with codecs.open(filename, 'w', encoding="utf8") as handle:
            handle.write(
                json.dumps(self.data, sort_keys=True, indent=2, separators=(',', ': '), ensure_ascii=False)
            )


class Parser(object):
    def is_language(self, adict):
        expected = [
            u'checkedby', u'language', u'classification', u'author',
            u'silcode', u'notes', u'typedby', u'id', u'problems'
        ]
        return all([e in adict.keys() for e in expected])

    def is_lexicon(self, adict):
        expected = [
            u'cognacy', u'word', u'loan', u'id',
            u'item', u'pmpcognacy', u'annotation', u'word_id'
        ]
        return all([e in adict.keys() for e in expected])

    def is_location(self, adict):
        expected = ['latitude', 'longitude']
        return all([e in adict.keys() for e in expected])

    def parse(self, content):
        xml = minidom.parseString(XMLTEMPLATE % content)
        entities = {'language': None, 'lexicon': [], 'location': None}
        for node in xml.getElementsByTagName('record'):
            content = {}
            for child in node.childNodes:
                # skip text nodes (which are whitespace indentation)
                if child.nodeType == child.TEXT_NODE:
                    continue

                tag = child.tagName
                assert tag not in content

                try:
                    data = child.firstChild.data
                except AttributeError:
                    # no data e.g. <x></x>
                    data = None

                content[tag] = data
                
            if self.is_language(content):
                if entities['language'] is not None:
                    raise ValueError("Encountered Duplicate Language Record")
                entities['language'] = content
            elif self.is_lexicon(content):
                entities['lexicon'].append(content)
            elif self.is_location(content):
                entities['location'] = content
            else:
                raise ValueError("Unknown Record Type: %r" % content)

        # check
        if entities['language'] is None:
            raise ValueError("No Language Record Found!")
        if len(entities['lexicon']) == 0:
            raise ValueError("No Lexical Records Found!")

        return entities


class ABVDatabase(object):
    def __init__(self, files=None, check=True, strict=True, uniques=True):
        self.files = {}
        self.records = None
        # set cognate parser settings
        self.strict = strict
        self.uniques = uniques
        self.check = check
        if files:
            for f in files:
                self.load(f)
        
    def load(self, filename):
        with codecs.open(filename, 'r', encoding="utf8") as handle:
            self.files[filename] = json.load(handle, encoding="utf8")
    
    def get_details(self, filename):
        return self.files[filename]['language']

    def get_location(self, filename):
        return self.files[filename]['location']

    def get_lexicon(self, filename):
        return self.files[filename]['lexicon']

    def process(self):
        self.records = []
        CP = CognateParser(check=self.check, strict=self.strict, uniques=self.uniques)
        for filename in self.files:
            d = self.get_details(filename)
            for e in self.get_lexicon(filename):
                self.records.append(Record(
                    LID = int(d['id']),
                    ID = int(e['id']),
                    WID = int(e['word_id']),
                    Language = d['language'],
                    Word = e['word'],
                    Item = e['item'],
                    Annotation = e['annotation'],
                    Loan = e['loan'],
                    Cognacy = CP.parse_cognate(e['cognacy']),
                ))
        return self.records
        