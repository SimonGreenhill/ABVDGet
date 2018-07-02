#!/usr/bin/env python3
# coding=utf-8

import json
import codecs
from xml.dom import minidom
from functools import lru_cache

from abvdget.tools import slugify

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

DEAD_LANGUAGES = {
    'bantu': [],
    'mayan': [],
    'utoaztecan': [],
    'austronesian': [
        261,  # Futuna-Aniwa
        874,  # proto-philippines
    ],
}


class DeadLanguageError(ValueError):
    pass


class InvalidLanguageError(ValueError):
    pass


class Record(object):
    """Data Class for Lexical Records."""
    def __init__(self, ID=None, LID=None, WID=None, Language=None, Word=None, Item=None, Annotation=None, Loan=None, Cognacy=None):
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
        """Is this lexeme a loan."""
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
            return "%s_%d" % (slugify(self.Language), self.LID)



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
        language_id = self.is_valid_language(language_id)
        req = requests.get(self.make_url(language_id))
        
        # fail on no content
        if len(req.content) == 0 or req.content.strip() == 'null':
            raise InvalidLanguageError("Language %d does not exist" % language_id)
            
        try:
            content = req.content.decode('utf8')
        except:
            raise
            
        self.data = Parser().parse(content)
        return self.data
    
    def write(self, filename, content=None):  # pragma: no cover
        with codecs.open(filename, 'w', encoding="utf8") as handle:
            handle.write(json.dumps(
                content if content else self.data,
                sort_keys=True, indent=2,
                separators=(',', ': '), ensure_ascii=False
            ))
    
    def is_valid_language(self, language_id):
        if not isinstance(language_id, int):
            raise InvalidLanguageError("Language id must be an integer")
        if language_id in DEAD_LANGUAGES[self.database]:
            raise DeadLanguageError("Language %d has been removed" % language_id)
        return language_id
        
    def get_to_file(self, language_id, filename):  # pragma: no cover
        self.write(filename, self.get(language_id))


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
        self._lexicon_by_file = {}
        self.records = None
        
        if files:
            for f in files:
                self.load(f)
        
    def load(self, filename):
        with codecs.open(filename, 'r', encoding="utf8") as handle:
            self.files[filename] = json.load(handle, encoding="utf8")
    
    def get_details(self, filename):
        d = self.files[filename].get('language')
        if d is None:
            raise ValueError("Data for %s not loaded" % filename)
        d['filename'] = filename
        return d

    def get_location(self, filename):
        return self.files[filename]['location']

    def get_lexicon(self, filename):
        if filename not in self._lexicon_by_file:
            self._lexicon_by_file[filename] = []
            d = self.get_details(filename)
            for r in self.files[filename]['lexicon']:
                self._lexicon_by_file[filename].append(self.to_record(d, r))
        yield from self._lexicon_by_file[filename]
        
    @lru_cache(maxsize=2000)
    def get_nlexemes(self, filename):
        return len(list(self.get_lexicon(filename)))

    @lru_cache(maxsize=2000)
    def get_ncognates(self, filename):
        return len([
            r for r in self.get_lexicon(filename)
            if r.Cognacy is not None
        ])
    
    @lru_cache(maxsize=2000)
    def get_slug_for(self, taxon, id):
        return "%s_%s" % (slugify(taxon), id)
    
    def to_record(self, details, entry):
        return Record(
            LID=int(details['id']),
            ID=int(entry['id']),
            WID=int(entry['word_id']),
            Language=details['language'],
            Word=entry['word'],
            Item=entry['item'],
            Annotation=entry['annotation'],
            Loan=entry['loan'],
            Cognacy=entry['cognacy']
        )
    
    def process(self):
        self.records = []
        for filename in self.files:
            d = self.get_details(filename)
            self.records.extend(self.get_lexicon(filename))
        return self.records
    
    def save_details(self, filename):
        def denone(v):
            return '' if v is None else v

        def check_tabs(v):
            assert "\t" not in v

        def fmt_loc(v):
            return "%0.4f" % float(v) if v != '-' else v
        
        with codecs.open(filename, 'w', encoding="utf8") as out:
            out.write("\t".join([
                "ID", "ISO", "Glottocode", "Language", "Slug", "NLexemes",
                "NCognates","Author", "Latitude", "Longitude", "Classification"
            ]))
            out.write("\n")
            for f in self.files:
                lang = self.get_details(f)
                loc = self.get_location(f)
                loc = {'longitude': '-', 'latitude': '-'} if loc is None else loc
                taxon = self.get_slug_for(lang['language'], lang['id'])
                line = [
                    lang['id'],
                    denone(lang['silcode']),
                    denone(lang['glottocode']),
                    lang['language'],
                    taxon,
                    '%d' % self.get_nlexemes(f),
                    '%d' % self.get_ncognates(f),
                    denone(lang['author']),
                    fmt_loc(loc['latitude']),
                    fmt_loc(loc['longitude']),
                    denone(lang['classification']),
                ]
                try:
                    [check_tabs(v) for v in line]
                except (AssertionError, TypeError):  # pragma: no cover
                    print("ERROR", line)
                    raise
                out.write("\t".join(line))
                out.write("\n")
        return
