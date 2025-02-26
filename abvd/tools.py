import unicodedata

def clean(var):
    """Removes tabs, newlines and trailing whitespace"""
    if var is None:
        return ''
    return var.replace("\t", "").replace("\n", "").strip()

def slugify(var):
    remove = ["(", ")", ";", "?", '’', "'", ".", ",", ':', "‘",]
    replace = [
        (" - ", '_'), (" ", "_"), ("ŋ", "ng"), ('ʝ', "j"),
        ('ɛ', 'e'), ('ʃ', 'sh'), ('ø', 'Y'), ('ɲ', 'nj'),
    ]
    var = var.split("[")[0].strip()
    var = var.split("/")[0].strip()
    var = unicodedata.normalize('NFKD', var)
    var = "".join([c for c in var if not unicodedata.combining(c)])
    var = var.replace("ß", "V")  # do this before casefolding
    var = var.casefold()
    for r in remove:
        var = var.replace(r, "")
    for r in replace:
        var = var.replace(*r)
    var = var.title()
    return var
