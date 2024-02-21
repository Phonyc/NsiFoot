from difflib import SequenceMatcher

from unidecode import unidecode


def similar(a, b):
    """ Similarité de 2 textes"""
    return SequenceMatcher(None, unidecode(a.lower()), unidecode(b.lower())).ratio()
