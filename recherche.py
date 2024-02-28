"""Module de recherche de joueur ou d'équipe"""
import pandas as pd

import dessins
import utils
import datas


def menu():
    """Menu de recherche de joueur ou d'équipe"""

    # On affiche la décoration et demande la recherche
    recherche = utils.show_banner("Recherche",
                                  "Veuillez rentrer une requête (la forme de la requête n'as pas d'importance)",
                                  emplacement="Menu > Recherche",
                                  demande="Entrez le nom du joueur ou de l'équipe à chercher (c pour revenir en "
                                          "arrière): ")
    if recherche == "c":
        return

    if recherche != "":
        # On effectue la recherche
        joueurs_recherche, clubs_recherche = compute_recherche(recherche)
        clubs_recherche.rename(columns={"name": "nom_prenom"}, inplace=True)

        # Affichage des résultats

        affichage, found, first_df, second_df = show_search_results(joueurs_recherche, clubs_recherche)

        message_choix_interne = ""
        # Choix de l'élément à afficher
        if not found:
            print(affichage)
            input("Appuyez sur Entrée pour continuer ...")
        elif affichage != "":
            while True:
                rep = utils.show_banner("Résultats Recherche",
                                        subtitle=f'"{recherche}"',
                                        emplacement="Menu > Recherche > Résultats de la Recherche",
                                        footer=affichage,
                                        alerte=message_choix_interne,
                                        demande="Entrez le numéro de l'élément dont vous voulez obtenir les infos. (c "
                                                "pour revenir en arrière): ")
                if rep == "c":
                    break

                try:
                    index = int(rep) - 1
                    if index < len(first_df):
                        show_stats(first_df.loc[index])
                    else:
                        show_stats(second_df.loc[index - len(first_df)])
                    break
                except ValueError:
                    message_choix_interne = "Choix invalide ! (Resultats de recherche)"

    menu()


def show_search_results(joueurs_recherche, clubs_recherche):
    """Crée l'affichage des résultats de recherche"""
    affichage = "\n"

    # On ne garde qu'un seul df s'il y a un écart trop important dans la qualité des résultats
    found, ecart, first_df, second_df = search_results_get_first_df(joueurs_recherche, clubs_recherche)

    assert len(first_df) >= len(second_df)

    # Si la réponse est sûre, on affiche directement les stats
    seuil_ecart = 0.1
    if len(first_df) == 1 and (len(second_df) == 0 or ecart > seuil_ecart):
        show_stats(first_df.loc[0])
        return "", True, first_df, second_df

    if not found:  # S'il n'y a pas de résultats
        return dessins.NO_RESULT_FOUND, found, first_df, second_df

    # Entêtes des colonnes
    ban1, ban2 = ("Joueurs Trouvés", "Equipes Trouvées") if "ville" not in list(first_df.columns) else (
        "Equipes Trouvées", "Joueurs Trouvés")

    # Listes des textes dans les colonnes
    f_list = []
    s_list = []

    # Largeur max de la colonne de gauche
    max_len_left = 0
    for index, row in first_df.iterrows():
        txt = f'\033[96m{index + 1}\033[0m. {row["nom_prenom"]}'
        max_len_left = max(max_len_left, len(txt))
        f_list.append(txt)

    max_len_left += 5

    for index, row in second_df.iterrows():
        print(len(f_list) + index + 1)
        txt = f'\033[96m{len(f_list) + index + 1}\033[0m. {row["nom_prenom"]}'
        s_list.append(txt)

    # On remplit les listes pour qu'elles aient la même taille
    s_list += ["\033[96m\033[0m"] * (len(f_list) - len(s_list))
    f_list += ["\033[96m\033[0m"] * (len(s_list) - len(f_list))

    if ecart < seuil_ecart:
        # On affiche les 2 listes
        len_color = len("\033[96m\033[0m")
        affichage += f'{ban1.ljust(max_len_left - len_color)}|      {ban2} \n'
        affichage += f'{(len(ban1) * "-").ljust(max_len_left - len_color)}|      {len(ban2) * "-"} \n'

        for f_elem, s_elem in zip(f_list, s_list):
            affichage += f'{f_elem.ljust(max_len_left)}|      {s_elem} \n'
    else:
        # On affiche qu'une liste
        affichage += f'{ban1}\n'
        affichage += f'{len(ban1) * "-"}\n'
        for f_list_elem in f_list:
            affichage += f'{f_list_elem}\n'

    return affichage, found, first_df, second_df


def search_results_get_first_df(joueurs_recherche, clubs_recherche):
    """Renvoie le df à afficher en premier et celui en second (en fonction des scores dedans)"""
    # On calcule un écart de score pour savoir si on affiche les deux df ou un seul
    ecart = 10
    found = True
    # Afficher en premier le df où il y a le score de ressemblance le plus grand
    second_df = pd.DataFrame()
    if len(joueurs_recherche) == 0 and len(clubs_recherche) == 0:
        found = False
        first_df = pd.DataFrame()
    elif len(joueurs_recherche) == 0:
        first_df = clubs_recherche
    elif len(clubs_recherche) == 0:
        first_df = joueurs_recherche
    else:
        first_df, second_df = (joueurs_recherche, clubs_recherche) if (joueurs_recherche.loc[0]["score"] >
                                                                       clubs_recherche.loc[0]["score"]) else (
            clubs_recherche, joueurs_recherche)
        ecart = first_df.loc[0]["score"] - second_df.loc[0]["score"]

    return found, ecart, first_df, second_df


def show_stats(element: pd.Series):
    """Afficher les statistiques d'un joueur ou d'une équipe"""
    utils.show_banner("Statistiques",
                      emplacement=f"Menu > Recherche > {element['nom_prenom']} > Statistiques")
    isjoueur = "ville" not in list(element.index)
    if isjoueur:

        noms = f"""
        `          .~~~.                                            
        `         |     |    Nom    : \033[00m\033[0m\033[96m{element['nom']}\033[0m
        `         ".___."    Prénom : \033[00m\033[0m\033[96m{element['prenom']}\033[0m
        `       .'       '.  Age    : \033[96m{element['age']}\033[0m ans (\033[36m{element['birthdate']}\033[0m)
        `       |         |  Club   : \033[00m\033[0m\033[96m{element['name_club']}\033[0m
        """
        max_line = 0
        for line in noms.split('\n'):
            max_line = max(max_line, len(line.strip()))
        unite_salaire = "M"
        salaire = element['salaire']
        if element['salaire'] < 1:
            salaire *= 1000
            unite_salaire = "K"
        physique = f"""

        Poids         : \033[96m{round(element['poids'])}\033[0m kg
        Taille        : \033[96m{round(element['taille'])}\033[0m cm
        Meilleur pied : \033[96m{element['meilleur pied'].replace("Right", "Droit").replace("Left", "Gauche")}\033[0m
        Salaire       : \033[96m{round(salaire, 3)} {unite_salaire}\033[0m € / mois
        """
        identite = ""
        for line_n, line_p in zip(noms.split('\n'), physique.split('\n')):
            identite += line_n.strip().ljust(max_line + 10) + line_p.strip() + "\n"

        stats_foot = f"""\n\n\n
                Nombre de matchs joués        : \033[96m{round(element['matchs_j'])}\033[0m

                Nombre de buts marqués        : \033[96m{round(element['buts_m_joueur'])}\033[0m
                Nombre de passes déscisives   : \033[96m{round(element['pass_d'])}\033[0m
                Nombre de buts encaissés      : \033[96m{round(element['buts_e_joueur'])}\033[0m\n\n
                """

        poste_dessin = dessins.POSTES[element["poste"]]

        foot = ""
        for line_p, line_s in zip(poste_dessin.split('\n'), stats_foot.split('\n')):
            foot += line_p.strip().ljust(50) + line_s.strip() + "\n"
        print(identite)
        print(foot)

    else:
        affichage_constr = f"""
        ` +----+----------+                       
        ` |    |  ~~~~~~~ |     Nom              : \033[96m{element['nom_prenom']}\033[0m (Ville : \033[36m{element['ville']}\033[0m)
        ` |----+  ~~~~    |     Date de création : \033[96m{element['date_crea']}\033[0m
        ` |       ~~~~~~  |     Nombre de titres : \033[96m{element['titres']}\033[0m
        ` +---------------+                   
        `
        `
        ` +---------------+                       
        ` |    Ligue 1    |     Rang : \033[96m{element['rang']}\033[0m
        ` |  (2022-2023)  |     Budget : \033[96m{element['budget']} M\033[0m €
        ` +---------------+     
        `                       Nombre de Victoires : \033[96m{element['victoires']}\033[0m
        `                       Nombre de Nuls      : \033[96m{element['nuls']}\033[0m
        `                       Nombre de Défaitres : \033[96m{element['defaites']}\033[0m
        `                       
        `                       Nombre de buts Marqués   : \033[96m{element['buts_m']}\033[0m
        `                       Nombre de buts Encaissés : \033[96m{element['buts_e']}\033[0m
        """
        for line in affichage_constr.split('\n'):
            print(line.strip())

    input("Appuyez sur Entrée pour continuer ...")


def compute_recherche(recherche: str):
    """Permet de rechercher un joueur ou une équipe de façon plutôt efficace"""
    # Seuil de tolérance de ressemblance
    seuil = 0.7

    # On copie les df pour ne pas les modifier
    joueurs_recherche = datas.joueurs_df.copy(deep=True)
    clubs_recherche = datas.clubs_df.copy(deep=True)

    if " " in recherche:  # Si le nom est complet (nom et prénom)
        # On ajoute une colonne qui contient un score de ressemblance entre le nom complet et la recherche
        joueurs_recherche.insert(0, "score", joueurs_recherche.apply(
            lambda joueur: max(utils.similar(f'{joueur["nom"]} {joueur["prenom"]}', recherche),
                               utils.similar(f'{joueur["prenom"]} {joueur["nom"]}', recherche)), axis=1))

    else:  # Si le nom est incomplet (nom ou prénom)
        # On effectue le même procédé
        joueurs_recherche.insert(0, "score", joueurs_recherche.apply(
            lambda joueur: max(utils.similar(f'{joueur["nom"]}', recherche),
                               utils.similar(f'{joueur["prenom"]}', recherche)), axis=1))

    joueurs_recherche = joueurs_recherche[joueurs_recherche['score'] > seuil]

    # Recherche dans les clubs
    clubs_recherche.insert(0, "score", clubs_recherche.apply(
        lambda club: max(utils.similar(f'{club["name"]}', recherche), utils.similar(f'{club["short_name"]}', recherche),
                         utils.similar(f'{club["ville"]}', recherche), ), axis=1))

    clubs_recherche = clubs_recherche[clubs_recherche['score'] > seuil]

    # On trie les résultats par score et on réinitialise l'index
    joueurs_recherche.sort_values(by="score", ascending=False, inplace=True)
    clubs_recherche.sort_values(by="score", ascending=False, inplace=True)

    joueurs_recherche.reset_index(drop=True, inplace=True)
    clubs_recherche.reset_index(drop=True, inplace=True)

    result_search_reduce(joueurs_recherche)
    result_search_reduce(clubs_recherche)

    return joueurs_recherche, clubs_recherche


def result_search_reduce(df):
    """Réduit les df de résultat en gardant les éléments tant qu'il n'y a pas un gros écart de score"""
    stop = False
    for index, row in df.iterrows():
        if not stop:
            if index != 0 and (df.iloc[index - 1]["score"] - row["score"] > 0.15 or
                               df.iloc[0]["score"] - row["score"] > 0.2):
                df.drop(index, inplace=True)
                stop = True
        else:
            df.drop(index, inplace=True)
