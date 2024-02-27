"""
 _  _      _  ___            _   
| \| | ___(_)| __| ___  ___ | |_ 
| .  |(_-/| || _| / _ \/ _ \|  _|
|_|\_|/__/|_||_|  \___/\___/ \__|
"""
from difflib import SequenceMatcher

from unidecode import unidecode
import os


def similar(a, b):
    """ Similarité de 2 textes"""
    return SequenceMatcher(None, unidecode(a.lower()), unidecode(b.lower())).ratio()


def term_size():
    """Récupérer la taille du terminal"""
    try:
        ts = os.get_terminal_size()
        return ts.columns, ts.lines
    except:
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


PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'

print("\033[1;31m" + "Votre texte ici" + "\033[0m")
print("\033[31m" + "Votre texte ici" + "\033[0m")
print("\033[31m" + "Votre texte ici" + "\033[0m")
print("\033[1;31m*\033[0;31m: Paramètres disponibles uniquement en Abscisses\033[0m")