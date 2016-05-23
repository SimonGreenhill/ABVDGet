# ABVDGet

## Download data:

```
from abvdget import Downloader
content = Downloader('austronesian').get(1)

d = Downloader('austronesian')
d.get(99)
d.write("99.json")
```

## Process data into useable format:

```
db = ABVDatabase(
    strict=True,  # Strict cognate coding (i.e. ignore dubious items like 1?)
    uniques=True, # encode non-cognate items as unique states.
)
db.load('1.json')
db.load('2.json')
db.load('3.json')
db.process()
for r in db.records:
    print(r)
```
