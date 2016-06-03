import os
import unittest

from abvdget import CognateParser

class TestCognateParser(unittest.TestCase):
    
    def test_simple(self):
        self.assertEqual(CognateParser().parse_cognate('1'), [1])
        self.assertEqual(CognateParser().parse_cognate('10'), [10])
        self.assertEqual(CognateParser().parse_cognate('100'), [100])
        self.assertEqual(CognateParser().parse_cognate('111'), [111])
    
    def test_subset(self):
        self.assertEqual(CognateParser().parse_cognate('1,2'), [1, 2])
        self.assertEqual(CognateParser().parse_cognate('1   ,   2'), [1, 2])
        self.assertEqual(CognateParser().parse_cognate('1,2,3,4,5'), [1, 2, 3, 4, 5])
        self.assertEqual(CognateParser().parse_cognate('1, 17, 37'), [1, 17, 37])
        self.assertEqual(CognateParser().parse_cognate('1,10,66,67'), [1, 10, 66, 67])
    
    def test_dubious(self):
        self.assertEqual(CognateParser().parse_cognate('1?'), ['u_1'])
        self.assertEqual(CognateParser().parse_cognate('?'), ['u_1'])
        
    def test_dubious_subset(self):
        self.assertEqual(CognateParser().parse_cognate('1, 2?'), [1])
        self.assertEqual(CognateParser().parse_cognate('1?, 2'), [2])
        self.assertEqual(CognateParser().parse_cognate('91?, 42'), [42])
        self.assertEqual(CognateParser().parse_cognate('?, 31'), [31])
        # note that both of these are dubious, should become a unique 
        # state instead
        self.assertEqual(CognateParser().parse_cognate('1?, 2?'), ['u_1'])
    
    def test_bad_entries_uniques(self):
        # coded as x
        self.assertEqual(CognateParser(uniques=True).parse_cognate('X'), ['u_1'])
        self.assertEqual(CognateParser(uniques=True).parse_cognate('x'), ['u_1'])

    def test_bad_entries_nouniques(self):
        self.assertEqual(CognateParser(uniques=False).parse_cognate('X'), [])
        self.assertEqual(CognateParser(uniques=False).parse_cognate('x'), [])

    def test_s_entries_uniques(self):
        # entries that are in the wrong word (e.g. you sg. not you pl.)
        self.assertEqual(CognateParser(uniques=True).parse_cognate('s'), ['u_1'])

    def test_s_entries_nouniques(self):
        # entries that are in the wrong word (e.g. you sg. not you pl.)
        self.assertEqual(CognateParser(uniques=False).parse_cognate('s'), [])
    
    def test_add_unique(self):
        CP = CognateParser()
        self.assertEqual(CP.parse_cognate(''), ['u_1'])
        self.assertEqual(CP.parse_cognate(''), ['u_2'])
        self.assertEqual(CP.parse_cognate(''), ['u_3'])
        self.assertEqual(CP.parse_cognate(''), ['u_4'])

    def test_no_uniques(self):
        CP = CognateParser(uniques=False)
        self.assertEqual(CP.parse_cognate(''), [])
        self.assertEqual(CP.parse_cognate(''), [])
        self.assertEqual(CP.parse_cognate(''), [])
    
    def test_dubious_with_no_strict(self):
        self.assertEqual(CognateParser(strict=False).parse_cognate('1?'), [1])
        self.assertEqual(CognateParser(strict=False).parse_cognate('1, 2?'), [1, 2])
    
    def test_null(self):
        self.assertEqual(CognateParser().parse_cognate(None), ['u_1'])
    
    def test_bad_cog_alphabetical(self):
        with self.assertRaises(ValueError):
            CognateParser().parse_cognate('A')
    
    def test_checkFalse(self):
        CognateParser(check=False).parse_cognate('A') == ['A']
        CognateParser(check=False).parse_cognate('1, a') == ['1, a']
        CognateParser(check=False).parse_cognate('1a') == ['1a']
    
    def test_bad_cog_int(self):
        with self.assertRaises(ValueError):
            CognateParser().parse_cognate(1)
    
    def test_complicated_strict_unique(self):
        CP = CognateParser(strict=True, uniques=True)
        # # 3. right
        # Maori    katau         5, 40
        # Maori    matau         5
        # South Island Maori    tika          
        self.assertEqual(CP.parse_cognate('5, 40'), [5, 40])
        self.assertEqual(CP.parse_cognate('5'), [5])
        self.assertEqual(CP.parse_cognate(''), ['u_1'])
        
        # # 8. turn
        # Maori    huri         15
        # South Island Maori    tahuli         15
        # South Island Maori    tahuri    to turn, to turn around    15
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        
        # # 20. to know
        # Maori    moohio         52
        # South Island Maori    matau         1
        # South Island Maori    mohio    to know    52
        # South Island Maori    ara    to know, to awake     
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate('1'), [1])
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate(''), ["u_2"])

        # # 36: to spit
        # Maori    tuha         19, 34?
        # South Island Maori    huare         18
        # South Island Maori    tuha    to expectorate, to spit    19, 34?
        self.assertEqual(CP.parse_cognate('19, 34?'), [19])
        self.assertEqual(CP.parse_cognate('18'), [18])
        self.assertEqual(CP.parse_cognate('19, 34?'), [19])

    def test_complicated_nostrict_unique(self):
        CP = CognateParser(strict=False, uniques=True)
        # # 3. right
        # Maori    katau         5, 40
        # Maori    matau         5
        # South Island Maori    tika          
        self.assertEqual(CP.parse_cognate('5, 40'), [5, 40])
        self.assertEqual(CP.parse_cognate('5'), [5])
        self.assertEqual(CP.parse_cognate(''), ['u_1'])
        
        # # 8. turn
        # Maori    huri         15
        # South Island Maori    tahuli         15
        # South Island Maori    tahuri    to turn, to turn around    15
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        
        # # 20. to know
        # Maori    moohio         52
        # South Island Maori    matau         1
        # South Island Maori    mohio    to know    52
        # South Island Maori    ara    to know, to awake     
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate('1'), [1])
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate(''), ["u_2"])

        # # 36: to spit
        # Maori    tuha         19, 34?
        # South Island Maori    huare         18
        # South Island Maori    tuha    to expectorate, to spit    19, 34?
        self.assertEqual(CP.parse_cognate('19, 34?'), [19, 34])
        self.assertEqual(CP.parse_cognate('18'), [18])
        self.assertEqual(CP.parse_cognate('19, 34?'), [19, 34])

    def test_complicated_nostrict_nounique(self):
        CP = CognateParser(strict=False, uniques=False)
        # # 3. right
        # Maori    katau         5, 40
        # Maori    matau         5
        # South Island Maori    tika          
        self.assertEqual(CP.parse_cognate('5, 40'), [5, 40])
        self.assertEqual(CP.parse_cognate('5'), [5])
        self.assertEqual(CP.parse_cognate(''), [])
        
        # # 8. turn
        # Maori    huri         15
        # South Island Maori    tahuli         15
        # South Island Maori    tahuri    to turn, to turn around    15
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        self.assertEqual(CP.parse_cognate('15'), [15])
        
        # # 20. to know
        # Maori    moohio         52
        # South Island Maori    matau         1
        # South Island Maori    mohio    to know    52
        # South Island Maori    ara    to know, to awake     
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate('1'), [1])
        self.assertEqual(CP.parse_cognate('52'), [52])
        self.assertEqual(CP.parse_cognate(''), [])

        # # 36: to spit
        # Maori    tuha         19, 34?
        # South Island Maori    huare         18
        # South Island Maori    tuha    to expectorate, to spit    19, 34?
        self.assertEqual(CP.parse_cognate('19, 34?'), [19, 34])
        self.assertEqual(CP.parse_cognate('18'), [18])
        self.assertEqual(CP.parse_cognate('19, 34?'), [19, 34])
        
        
        
if __name__ == '__main__':
    unittest.main()


