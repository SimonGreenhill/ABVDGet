import unicodedata

def clean(var):
    """Removes tabs, newlines and trailing whitespace"""
    if var is None:
        return ''
    return var.replace("\t", "").replace("\n", "").strip()


def slugify(var):
    var = var.split("[")[0].strip()
    var = var.split("/")[0].strip()
    var = var.replace("(", "").replace(")", "")
    var = unicodedata.normalize('NFKD', var)
    var = "".join([c for c in var if not unicodedata.combining(c)])
    var = var.replace(" - ", "_").replace("-", "")
    var = var.replace(":", "").replace('?', "")
    var = var.replace('’', '').replace("'", "")
    var = var.replace(',', "").replace(".", "")
    var = var.replace(" ", "_")
    var = var.replace("ß", "V")
    return var
