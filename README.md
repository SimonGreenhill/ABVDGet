# ABVDGet

## Download data:

```
from abvd import Downloader
content = Downloader('austronesian').get(1)

d = Downloader('austronesian')
d.get(99)
d.write("99.json")
```

## Process data into useable format:

```
db = ABVDatabase(files=['1.json', '2.json'])
db.process()
for r in db.records:
    print(r)
```
