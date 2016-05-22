import os
import unittest

from abvdget import ABVDatabase

TESTDATA = os.path.join(os.path.dirname(__file__), 'nengone.json')

EXPECTED = {
    99: {
        "LID": 99,
        "Annotation": "arm and hand",
        "Cognacy": [1],
        "Item": "nin",
        "Loan": None,
        "Word": "hand",
        "WID": 1
    }, 
    93340: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": [13],
        "Item": "iñtërnâtiônàlizætiøn",
        "Loan": None,
        "Word": "leg/foot",
        "WID": 4,
    },
    90697: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": ['u_1'],  # unique
        "Item": "kaka",
        "Loan": None,
        "Word": "to eat",
        "WID": 37
    },
    70785: {
        "LID": 99,
        "Annotation": None,
        "Cognacy": [1],
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
    
    def test_process(self):
        for r in self.abvd.process():
            assert r.ID in EXPECTED
            for k in EXPECTED[r.ID]:
                self.assertEqual(
                    EXPECTED[r.ID][k],
                    getattr(r, k)
                )

