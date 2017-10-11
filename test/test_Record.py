import unittest

from abvdget import Record

class TestRecord(unittest.TestCase):
    
    def test_simple(self):
        r = Record(ID=1, WID=2, LID=3, Language='English', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
        assert r.ID == 1
        assert r.WID == 2
        assert r.LID == 3
        assert r.Language == 'English'
        assert r.Word == 'Hand'
        assert r.Item == 'hand'
        assert r.Annotation == '?'
        assert r.Loan == "L"
        assert r.Cognacy == None
    
    def test_is_loan(self):
        assert not Record(Loan="").is_loan
        assert not Record(Loan=None).is_loan
        
        assert Record(Loan="L").is_loan
        assert Record(Loan="English").is_loan
        assert Record(Loan=True).is_loan
    
    def test_get_taxon(self):
        r = Record(ID=1, WID=2, LID=3, Language='English', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
        assert r.get_taxon() == "English_3"
        r = Record(ID=1, WID=2, LID=None, Language='English', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
        assert r.get_taxon() == "English"
    
    def test_get_taxon_spaces(self):
       r = Record(ID=1, WID=2, LID=583, Language='Arosi (Oneibia Village)', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
       assert r.get_taxon() == "Arosi_Oneibia_Village_583"
      
    def test_get_taxon_unicode(self):
       r = Record(ID=1, WID=2, LID=1502, Language='Wamoaŋ', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
       assert r.get_taxon() == "Wamoang_1502"
    
    def test_repr(self):
       r = Record(ID=1, WID=2, LID=3, Language='English', Word='Hand', Item='hand', Annotation='?', Cognacy=None, Loan="L")
       repr(r)
      
