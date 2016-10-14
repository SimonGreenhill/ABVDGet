import os
import sys
import codecs

sys.path.append('../../abvdget')
from CognateParser import CognateParser

FILELIST = ['austronesian.dat', 'mayan.dat', 'utoaztecan.dat']

CPs = CognateParser(strict=True, uniques=True, check=True)
CPw = CognateParser(strict=False, uniques=False, check=True)

def check(parser, cognate):
    try:
        return parser.parse_cognate(cognate)
    except:
        return
    
def _repr(v1, v2):
    return '✓' if v1 is not None and v2 is not None else 'X'
    

good, checked = 0, 0
for filename in FILELIST:
    subset = os.path.splitext(filename)[0]
    with codecs.open(filename, 'r', encoding="utf8") as handle:
        for line in handle:
            line = line.strip("\n")
            a = check(CPs, line)
            b = check(CPw, line)
            if a is None or b is None:
                print("%s \t %s  \t  %s  \t %15r \t %15r" % (
                    subset.ljust(20), _repr(a, b), line.ljust(10), a, b
                ))
            else:
                good += 1
            checked += 1
        
print("")
print("%d/%d are good (%0.2f)" % (good, checked, (good/checked)*100))

