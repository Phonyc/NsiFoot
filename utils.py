"""
 _  _      _  ___            _   
| \| | ___(_)| __| ___  ___ | |_ 
| .  |(_-/| || _| / _ \/ _ \|  _|
|_|\_|/__/|_||_|  \___/\___/ \__|
"""
import os
from difflib import SequenceMatcher

table_chars_decod = (
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
    '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ' ', '!', 'C/', 'PS', '$?', 'Y=', '|', 'SS', '"', '(c)',
    'a', '<<', '!', '', '(r)', '-', 'deg', '+-', '2', '3', "'", 'u', 'P', '*', ',', '1', 'o', '>>', ' 1/4', ' 1/2',
    ' 3/4', '?', 'A', 'A', 'A', 'A', 'A', 'A', 'AE', 'C', 'E', 'E', 'E', 'E', 'I', 'I', 'I', 'I', 'D', 'N', 'O', 'O',
    'O', 'O', 'O', 'x', 'O', 'U', 'U', 'U', 'U', 'Y', 'Th', 'ss', 'a', 'a', 'a', 'a', 'a', 'a', 'ae', 'c', 'e', 'e',
    'e', 'e', 'i', 'i', 'i', 'i', 'd', 'n', 'o', 'o', 'o', 'o', 'o', '/', 'o', 'u', 'u', 'u', 'u', 'y', 'th', 'y')


def my_unidecode(string: str) -> str:
    """Enlève les accents d'une chaîne de caractères, d'après le module unidecode"""
    new_string = ""

    for character in string:
        if ord(character) < 0x80:
            new_string += str(character)
        else:
            try:
                new_string += table_chars_decod[ord(character)] or character
            except IndexError:
                new_string += "?"

    return new_string


def similar(a, b):
    """ Similarité de 2 textes"""
    return SequenceMatcher(None, my_unidecode(a.lower()), my_unidecode(b.lower())).ratio()


def term_size():
    """Récupérer la taille du terminal"""
    try:
        ts = os.get_terminal_size()
        return ts.columns, ts.lines
    except:
        # TODO Message
        return 80, 24


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_banner(title: str, subtitle="", emplacement="", header="", footer="", demande="", alerte=""):
    # Vider le terminal 
    clear_console()

    print(header)

    # Récupérer la taille du terminal
    w, _ = term_size()

    # Afficher le titre
    print(f"{'=' * w}\n")
    print(f"\033[1m{title.center(w)}\033[0m")
    print(subtitle.center(w))
    if emplacement != "":
        print(f"\033[90m{emplacement}\033[0m")
        print(f"{'=' * w}")
    else:
        print(f"\n{'=' * w}")

    print(footer)

    if demande != "":
        print(f"\033[1;31m{alerte}\033[0m")
        return input(demande).strip()
    else:
        return None
