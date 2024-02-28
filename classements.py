"""Module pour les classements"""
import datas
import utils


def menu(message=""):
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

    choix = utils.show_page("Classement", "Entrez un paramètre par lequel classer les joueurs / les équipes",
                            emplacement="Menu > Classements",
                            footer=options_print,
                            demande="Entrez votre choix (c pour revenir en arrière): ", alerte=message)

    # Récupérer les choix
    try:
        int_choice = int(choix)
        if int_choice <= len(elems_joueurs):
            # On affiche le classement des joueurs
            afficher_classements(datas.joueurs_df, elems_joueurs[int_choice - 1])
        else:
            # On affiche le classement des clubs
            afficher_classements(
                datas.clubs_df, elems_clubs[int_choice - len(elems_joueurs) - 1])
        menu()
    except (ValueError, IndexError):
        if choix == "c":
            return
        else:
            menu("Choix invalide ! (Choix de classements)")


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

            insert = "\033[31m" if index >= len(sorted_df) - 2 and elem[0] == "rang" else ""
            insert2 = "\033[0m" if index >= len(sorted_df) - 2 and elem[0] == "rang" else ""

            table += (f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {insert}{row[col_name].ljust(max_len)}{insert2}"
                      f" : \033[96m{row[elem[0]]}\033[0m\n")

        table += "\nEn rouge : 2 derniers clubs relégués\n"
    # On affiche la table
    subt = ("Classement des equipes par " if col_name == "name" else "Classement des joueurs par ") + elem[1]
    choix = utils.show_page("Classement", subt,
                            emplacement="Menu > Classements > Classement",
                            footer=table,
                            demande="Appuyez Entrée pour continuer (* puis Entrée pour tout afficher) :")
    if choix == "*":
        afficher_classements(df, elem, True)
