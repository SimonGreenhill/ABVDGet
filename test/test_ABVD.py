import os
import unittest
import tempfile

from abvdget import ABVDatabase, Record

TESTDATA = os.path.join(os.path.dirname(__file__), 'nengone.json')

EXPECTED = {
    99: {
        "LID": 99,
        "Annotation": "arm and hand",
        "Cognacy": '1',
        "Item": "nin",
        "Loan": None,
        "Word": "hand",
        "WID": 1
    }, 
    93340: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": '13',
        "Item": "iñtërnâtiônàlizætiøn",
        "Loan": None,
        "Word": "leg/foot",
        "WID": 4,
    },
    90697: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": None,
        "Item": "kaka",
        "Loan": None,
        "Word": "to eat",
        "WID": 37
    },
    70785: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": '1',
        "Item": "tini",
        "Loan": None,
        "Word": "Three",
        "WID": 199
    }
}


class TestABVD(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.abvd = ABVDatabase(files=[TESTDATA])
    
    def test_load(self):
        assert TESTDATA in self.abvd.files
    
    def test_get_details(self):
        d = self.abvd.get_details(TESTDATA)
        assert d['id'] == '99'
        assert d['language'] == 'Nengone'
        assert d['silcode'] == 'nen'
        assert d['glottocode'] == 'neng1238'
    
    def test_get_details_injects_filename(self):
        d = self.abvd.get_details(TESTDATA)
        assert d.get('filename') == TESTDATA
    
    def test_get_location(self):
        d = self.abvd.get_location(TESTDATA)
        assert d['latitude'] == "-21.53484700204878876661"
        assert d['longitude'] == "167.98095703125000000000"
    
    def test_get_nlexemes(self):
        assert self.abvd.get_nlexemes(TESTDATA) == 4

    def test_get_ncognates(self):
        assert self.abvd.get_ncognates(TESTDATA) == 3
    
    def test_process(self):
        for r in self.abvd.process():
            assert r.ID in EXPECTED
            for k in EXPECTED[r.ID]:
                self.assertEqual(EXPECTED[r.ID][k], getattr(r, k))
    
    def test_get_slug_for(self):
        self.assertEqual(self.abvd.get_slug_for('Nengone', '99'), 'Nengone_99')
    
    def test_save_details(self):
        with tempfile.NamedTemporaryFile() as out:
            self.abvd.save_details(out.name)
            out.seek(0)
            content = out.readlines()
        assert len(content) == 2  # two lines, header and Nengone
