"""Programme de présentation de statistiques de la ligue 1 pour 2023"""
import datas
import dessins
import graphiques

import utils
import recherche


# TODO ajouter les relégations etc


def main(message=""):
    """Menu principal"""
    # Afficher le menu principal
    first_choice = utils.show_banner("Menu principal", "Veuillez choisir une option", emplacement="Menu",
                                     header=dessins.HEADER,
                                     footer=dessins.MAIN_OPTIONS, demande="Entrez votre choix (Ctrl+C pour quitter): ",
                                     alerte=message)
    # Récupérer les choix
    if first_choice == "1":
        recherche.menu()
    elif first_choice == "2":
        choix_classements()
    elif first_choice == "3":
        graphiques.menu()
    else:
        main("Choix invalide ! (Menu Principal)")


def choix_classements(message=""):
    """Menu pour choisir un classement à afficher"""

    # On crée l'affichage des options
    elems_joueurs = [("age", "Age"), ("poids", "Poids (en kg)"), ("taille", "Taille (en cm)"),
                     ("salaire", "Salaire (en M€)"),
                     ("buts_m_joueur", "Nombre de buts marqués"),
                     ("pass_d", "Nombre de passes décisives"),
                     ("buts_e_joueur", "Nombre de buts encaissés"), ("matchs_j",
                                                                     "Nombre de matchs joués"),
                     ]
    elems_clubs = [("date_crea", "Date de création"), ("rang", "Rang (+ relégations)"), ("budget", "Budget (en M€)"),
                   ("titres", "Nombre de titres"),
                   ("victoires", "Nombre de victoires"),
                   ("nuls", "Nombre de nuls"),
                   ("defaites", "Nombre de défaites"),
                   ("buts_m", "Nombre de buts marqués"),
                   ("buts_e", "Nombre de buts encaissés"),
                   ("rendement", "Rendement"),
                   ("domination", "Domination")]

    options_print = "\033[31mClassements des joueurs\033[0m\n"
    for index_class, classement_elem in enumerate(elems_joueurs):
        options_print += f"\033[96m{index_class + 1}\033[0m. {classement_elem[1]}\n"

    options_print += "\n\033[31mClassements des clubs\033[0m\n"
    for index_class, classement_elem in enumerate(elems_clubs):
        options_print += f"\033[96m{len(elems_joueurs) + index_class + 1}\033[0m. {classement_elem[1]}\n"

    choix = utils.show_banner("Classement", "Entrez un paramètre par lequel classer les joueurs / les équipes",
                              emplacement="Menu > Classements",
                              footer=options_print,
                              demande="Entrez votre choix (c pour revenir en arrière): ", alerte=message)

    # Récupérer les choix
    try:
        int_choice = int(choix)
        if int_choice <= len(elems_joueurs):
            # On envoie à la consruction de graphiques personnalisés
            afficher_classements(datas.joueurs_df, elems_joueurs[int_choice - 1])
            choix_classements()
        else:
            afficher_classements(
                datas.clubs_df, elems_clubs[int_choice - len(elems_joueurs) - 1])
            choix_classements()
    except (ValueError, IndexError):
        if choix == "c":
            main()
        else:
            choix_classements("Choix invalide ! (Choix de classements)")


def afficher_classements(df, elem, show_all=False):
    """Afficher les classements"""

    # Savoir quelle colonne aller chercher pour le nom
    col_name = "name" if "name" in df.columns else "nom_prenom"

    # Obtenir la plus grande largeur de nom_prenom
    max_len = df[col_name].apply(len).max()
    # Remplir la table
    table = ""

    sorted_df = df.sort_values(by=elem[0], ascending=elem[0] in [
        "rang"]).reset_index(drop=True)
    if show_all:
        for index, row in sorted_df.iterrows():
            table += (f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m"
                      f"{row[elem[0]]}\033[0m\n")
    else:
        for index, row in sorted_df.head(10).iterrows():
            table += (f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m"
                      f"{row[elem[0]]}\033[0m\n")
        table += "\n\033[33m...\033[0m\n\n"
        for index, row in sorted_df.tail(10).iterrows():
            table += (f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m"
                      f"{row[elem[0]]}\033[0m\n")

    # On affiche la table
    subt = ("Classement des equipes par " if col_name == "name" else "Classement des joueurs par ") + elem[1]
    choix = utils.show_banner("Classement", subt,
                              emplacement="Menu > Classements > Classement",
                              footer=table,
                              demande="Appuyez Entrée pour continuer (* puis Entrée pour tout afficher) :")
    if choix == "*":
        afficher_classements(df, elem, True)


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


if __name__ == "__main__":
    # width_term_guide()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Sortie")
