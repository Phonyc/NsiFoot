"""Programme de présentation de statistiques de la ligue 1 pour 2023"""
import os

import classements
import dessins
import graphiques
import recherche
import utils


def main(message=""):
    """Menu principal"""
    # Afficher le menu principal
    first_choice = utils.show_page("Menu principal", "Veuillez choisir une option", emplacement="Menu",
                                   header=dessins.HEADER,
                                   footer=dessins.MAIN_OPTIONS, demande="Entrez votre choix (Ctrl+C pour quitter): ",
                                   alerte=message)
    # Récupérer les choix
    if first_choice == "1":
        recherche.menu()
    elif first_choice == "2":
        classements.menu()
    elif first_choice == "3":
        graphiques.menu()
    else:
        main("Choix invalide ! (Menu Principal)")


def width_term_guide(re=False):
    """Guide pour l'élargissement du terminal"""
    utils.clear_console()
    w, h = utils.term_size()
    # Verif width
    confort = w >= 120 and h >= 33
    fonc = w >= 87

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
            utils.clear_console()
            print("_")
            print("\033[32m" + ("#\n" * 33)[:-1] + "~" + "\033[0m")
            print("\033[32m" + "=" * 121 + "\033[0m\n")
            print("\033[31m" + "=" * 88 + "\033[0m")

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
        cont = input("Pour continuer quand même, entrez \"Continuer\" sinon n'entrez rien : ")
        if cont.lower() == "continuer":
            return True
        return False


if __name__ == "__main__":
    try:
        if check_terminal():
            width_term_guide()
            while True:
                main()
    except KeyboardInterrupt:
        print("Sortie")
