"""
 _  _      _  ___            _   
| \| | ___(_)| __| ___  ___ | |_ 
| .  |(_-/| || _| / _ \/ _ \|  _|
|_|\_|/__/|_||_|  \___/\___/ \__|
"""
from difflib import SequenceMatcher

from unidecode import unidecode
import os
import rich


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


def show_banner(title: str, subtitle="", emplacement="", header="", footer="", demande="", alerte="", hrich=False,
                frich=False):
    # Vider le terminal 
    clear_console()

    if hrich:
        rich.print(header)
    else:
        print(header)

    # Récupérer la taille du terminal
    w, _ = term_size()

    # Afficher le titre
    print(f"{'=' * w}\n")
    rich.print(f"[bold]{title.center(w)}[/bold]")
    print(subtitle.center(w))
    if emplacement != "":
        rich.print(f"[bright_black]{emplacement}[/bright_black]")
        print(f"{'=' * w}")
    else:
        print(f"\n{'=' * w}")

    if frich:
        rich.print(footer)
    else:
        print(footer)

    if demande != "":
        rich.print(f"[bold][red]{alerte}[/red][/bold]")
        return input(demande).strip()
    else:
        return None
