from pandas import isnull

class CognateParser(object):
    def __init__(self, strict=True, uniques=True):
        """
        Parses cognates. 
        
        - strict (default=True):  remove dubious cognates (?)
        - uniques (default=True): non-cognate items get unique states
        """
        self.unique_id = 0
        
    def get_next_unique(self):
        if not self.uniques:
            return None
        self.unique_id = self.unique_id + 1
        return "u_%d" % self.unique_id
    
    def parse_cognate(self, value, strict=True):
        raw = value
        if isnull(value):
            return [self.get_next_unique()]
        elif value == '':
            return [self.get_next_unique()]
        elif value == 's':
            return []   # error
        elif isinstance(value, str):
            value = value.replace('.', ',')
            # parse out subcognates
            value = [v.strip() for v in value.split(",")]
        
            if strict:
                # remove dubious cognates
                value = [v for v in value if '?' not in v]
                # exit if all are dubious, setting to unique state
                if len(value) == 0:
                    return [self.get_next_unique()]
            else:
                value = [v.replace("?", "") for v in value]
        
            # remove BAD cognates (i.e. where entries are wrong
            value = [v for v in value if v.lower() != 'x']
            # remove any empty things in the list
            value = [v for v in value if len(v) > 0]
        
            try:
                value = [int(v) for v in value]
            except:
                raise ValueError("Cognate is incorrect: %r" % raw)
        
            return value
        else:
            raise ValueError("%s" % type(value))


