"""Programme de présentation de statistiques de la ligue 1 pour 2023"""

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


if __name__ == "__main__":
    try:
        # Check terminal
        if utils.check_terminal():
            utils.width_term_guide()

            # Boucle menu
            while True:
                try:
                    main()
                except KeyboardInterrupt:
                    print("Sortie")
                    break
                except Exception as e:
                    main(f"Désolé, Une erreur est survenue ... ({e})")

    except KeyboardInterrupt:
        print("Sortie")
