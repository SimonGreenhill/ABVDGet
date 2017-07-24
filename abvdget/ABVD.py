#!/usr/bin/env python3
#coding=utf-8

import json
import codecs
from xml.dom import minidom
from functools import lru_cache

try:
    import requests
except ImportError:  # pragma: no cover
    pass


URL = "http://abvd.shh.mpg.de/utils/save/?type=xml&section=%(db)s&language=%(id)d"


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



class Record(object):
    def __init__(self,
        ID=None, LID=None, WID=None, Language=None, Word=None, Item=None,
        Annotation=None, Loan=None, Cognacy=None
    ):
        self.ID = ID
        self.LID = LID
        self.WID = WID
        self.Language = Language
        self.Word = Word
        self.Item = Item
        self.Annotation = Annotation
        self.Loan = Loan
        self.Cognacy = Cognacy
    
    def __repr__(self):
        return "<Record %s - %s - %s - %s>" % (
            self.ID, self.Language, self.Word, self.Item
        )
    
    @property
    def is_loan(self):
        if self.Loan is None:
            return False
        elif self.Loan in (False, ""):
            return False
        elif self.Loan is True:
            return True
        else:
            return True
    
    def get_taxon(self):
        if self.LID is None:
            return self.Language
        else:
            return "%s_%d" % (self.Language, self.LID)



class Downloader(object):
    
    databases = DATABASES
    
    def __init__(self, database, url=URL):
        if database not in self.databases:
            raise ValueError("Unknown Database: %s" % database)
        self.database = database
        self.data = None
        self.url = URL
        
    def make_url(self, language_id):
        try:
            language_id = int(language_id)
        except:
            raise TypeError("language_id needs to be an integer")
        
        return self.url % {'db': self.database, 'id': language_id}
    
    @lru_cache(maxsize=2000)
    def get(self, language_id):  # pragma: no cover
        req = requests.get(self.make_url(language_id))
        
        # fail on no content
        if len(req.content) == 0:
            return None
        
        try:
            content = req.content.decode('utf8')
        except:
            raise
            
        self.data = Parser().parse(content)
        return self.data
    
    def write(self, filename):  # pragma: no cover
        with codecs.open(filename, 'w', encoding="utf8") as handle:
            handle.write(json.dumps(
                self.data, sort_keys=True, indent=2,
                separators=(',', ': '), ensure_ascii=False
            ))


class Parser(object):
    def is_language(self, adict):
        expected = [
            'id', 'checkedby', 'language', 'classification', 'author',
            'silcode', 'glottocode', 'notes', 'typedby', 'problems'
        ]
        return all([e in adict.keys() for e in expected])

    def is_lexicon(self, adict):
        expected = [
            'id', 'word_id', 'word',
            'item', 'annotation', 'loan', 'cognacy', 'pmpcognacy',
        ]
        return all([e in adict.keys() for e in expected])
    
    def is_lexicon_2(self, adict):
        expected = [
            'id', 'word_id', 'word',
            'source_id', 'source',
            'item', 'annotation', 'loan', 'cognacy',
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
            elif self.is_lexicon_2(content):
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
    def __init__(self, files=None):
        self.files = {}
        self.records = None
        
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
        for filename in self.files:
            d = self.get_details(filename)
            for e in self.get_lexicon(filename):
                self.records.append(Record(
                    LID=int(d['id']),
                    ID=int(e['id']),
                    WID=int(e['word_id']),
                    Language=d['language'],
                    Word=e['word'],
                    Item=e['item'],
                    Annotation=e['annotation'],
                    Loan=e['loan'],
                    Cognacy=e['cognacy'],
                ))
        return self.records
        