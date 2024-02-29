"""Module de fonctions utilitaires"""
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
    """Enlève les accents d'une chaîne de caractères,
    d'après le module unidecode (https://github.com/avian2/unidecode/tree/master/unidecode)"""
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
    except OSError:
        return 80, 24


def clear_console():
    """Vider le terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')


def show_page(title: str, subtitle="", emplacement="", header="", footer="", demande="", alerte=""):
    """Afficher une page"""
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


def width_term_guide(re=False):
    """Guide pour l'élargissement du terminal"""
    clear_console()
    w, h = term_size()
    # Verif width
    confort = w >= 120 and h >= 33
    fonc = w >= 94

    if (not fonc) or (not confort):
        if re:
            print(f"\033[31mVotre terminal est trop petit pour un affichage {'confortable' if fonc else 'fonctionnel'}"
                  f"\033[0m")
            resp = input("Voulez-vous vraiment continuer ? (o/n): ")
            if resp.lower() == "o":
                return
            else:
                width_term_guide()
        else:
            clear_console()
            print("_")
            print("\033[32m" + ("#\n" * 33)[:-1] + "~" + "\033[0m")
            print("\033[32m" + "=" * 121 + "\033[0m\n")
            print("\033[31m" + "=" * 95 + "\033[0m")

            print("")
            print(
                "\033[1mAgrandissez votre terminal pour augmenter l'expérience de navigation\033[0m")
            print(
                "Agrandissez jusqu'a ce que les lignes tiennent complètement sur une ligne (idem pour les colonnes)")
            print("Ligne \033[31mrouge\033[0m : Affichage fonctionnel")
            print("Ligne \033[32mverte\033[0m : Affichage confortable\n")

        input("Appuyez sur Entrée quand vous avez fini ...")
        width_term_guide(True)


def check_terminal():
    """Vérifier que le terminal est pris en charge"""
    try:
        _ = os.get_terminal_size()
        return True
    except OSError:
        print("Vous êtes sûrement dans un terminal intégré à un IDE, veuillez utiliser un terminal classique.")
        cont = input(
            "Pour continuer quand même, entrez \"Continuer\" sinon n'entrez rien : ")
        if cont.lower() == "continuer":
            return True
        return False
