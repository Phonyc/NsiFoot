import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rich.console import Console
from rich.table import Table
import rich
import utils

# Constantes
HEADER = """
 _  _      _  ___            _   
| \| | ___(_)| __| ___  ___ | |_ 
| .  |(_-/| || _| / _ \/ _ \|  _|
|_|\_|/__/|_||_|  \___/\___/ \__|

Programme de présentation de statistiques de la ligue 1 pour 2023
"""
# Options en ascii art
MAIN_OPTIONS = """
   .....                                                                        
 ..     ..                        _______                    |              __  
.         .                      |   1   |                   |        /    |  | 
 ..     ..               _______ |       |                   |       / __  |  | 
   ..... ..             |   2   ||       | _______           |  /\  / |  | |  | 
          ...           |       ||       ||   3   |          | /  \/  |  | |  | 
            ..          |       ||       ||       |          |/_______|__|_|__|_

1. Rechercher           2. Afficher des classements          3. Afficher        
 (joueur/équipe)                                                des graphiques  

"""
GRAPH_WAIT = """
Préparation de votre graphique
        Patientez...
       
       #############
       a           a
       a   .....   a
        a ....... a
          a.....a
            a.a
          a  .  a
        a    .    a  
       a   .....   a
       a  ........ a   
       #############   
        
"""
# Charger les données des fichiers CSV
clubs_df = pd.read_csv("clubs.csv", delimiter=';')
joueurs_df = pd.read_csv("joueurs.csv", delimiter=';')

# Ajouter des variables fabriquées
clubs_df["rendement"] = 1 / (clubs_df["rang"] * clubs_df["budget"])
clubs_df["domination"] = ((100 * clubs_df["titres"]) / (2023 - clubs_df["date_crea"]))

# Modification du type de la date de création en str pour l'affichage dans les graphiques
clubs_df[["date_crea"]] = clubs_df[["date_crea"]].astype(str)

# Merge du df joueurs avec celui club

# Pour Ajouter "_club" à toutes les colonnes ayant été mergées
col_origin = list(joueurs_df.columns)

# Merge
joueurs_df = pd.merge(joueurs_df, clubs_df, left_on='club', right_on='id', how='left', suffixes=('_joueur', '_club'),
                      validate="many_to_one")

# Renommage des colonnes
cols_nw = list(joueurs_df.columns)
for col in cols_nw:
    if col not in col_origin and not col.endswith("_club") and not col.endswith("_joueur"):
        joueurs_df.rename(columns={col: col + "_club"}, inplace=True)

# Création de la variable âge du joueur (pour l'année 2023)
joueurs_df.insert(0, "age", joueurs_df.apply(lambda jx: 2023 - int(jx["birthdate"][:4]), axis=1))

# Création de la variable contenant à la fois le nom et le prénom à es fins de tri par ordre alphabétique
joueurs_df.insert(0, "nom_prenom", joueurs_df.apply(lambda jx: f"{jx['nom']} {jx['prenom']}", axis=1))

# Tri par ordre alphabétique + remise à zero de l'index après le tri
joueurs_df.sort_values(by="nom_prenom", inplace=True)
joueurs_df.reset_index(drop=True, inplace=True)


def main(message=""):
    """Menu principal"""
    # Afficher le menu principal
    first_choice = utils.show_banner("Menu principal", "Veuillez choisir une option", emplacement="Menu", header=HEADER,
                                     footer=MAIN_OPTIONS, demande="Entrez votre choix (Ctrl+C pour quitter): ",
                                     alerte=message)
    # Récupérer les choix
    if first_choice == "1":
        rechercher()
    elif first_choice == "2":
        afficher_classements()
    elif first_choice == "3":
        choix_construction_graphique()
    else:
        main("Choix invalide ! (Menu Principal)")


def afficher_classements():
    """Afficher les classements"""
    print("classements")


def choix_construction_graphique(message=""):
    """Menu pour choisir entre des graphiques recommandés ou des graphiques personnalisés"""

    # Elements transmis pour les graphiques personnalisés
    elements = [("Nom du joueur", False, True, "nom_prenom"), ("Poste", False, True, "poste"),
                ("Age", True, True, "age"), ("Poids (en kg)", True, True, "poids"),
                ("Taille (en cm)", True, True, "taille"),
                ("Salaire mensuel (en Millions d'euros)", True, True, "salaire"),
                ("Nombre de buts encaissés", True, True, "buts_e_joueur"),
                ("Nombre de buts Marqués", True, True, "buts_m_joueur"),
                ("Nombre de matchs joués", True, True, "matchs_j"),
                ("Meilleur pied", False, True, "meilleur pied"), ("Nombre de passes décisives", True, True, "pass_d"),
                ("Club", False, True, "name"), ("Rang (Club)", True, True, "rang"),
                ("Nombre de Victoires (Club)", True, True, "victoires"), ("Nombre de Nuls (Club)", True, True, "nuls"),
                ("Nombre de Défaites (Club)", True, True, "defaites"),
                ("Nombre de buts Marqués (Club)", True, True, "buts_m"),
                ("Nombre de buts encaissés (Club)", True, True, "buts_e"),
                ("Date de création du Club", False, True, "date_crea"),
                ("Budget du Club (en Milions d'euros)", True, True, "budget"),
                ("Nombre de titres du Club", True, True, "titres")]

    # Liste des graphiques recommandés
    # (Nom, Paramètre en abscisse, Paramètres en ordonnée)
    graphiques_recommandes = [("1. Nombre de buts marqués par club", 11, [16]),
                              (
                                  "2. Salaire moyen d'un joueur & Nombre de buts moyen marqués en fonction de son poste",
                                  1,
                                  [5, 7]),
                              ("3. Poids des joueurs en fonction de leur taille", 3, [4]),
                              ("4. Graphiques personnalisés", [], []), ]

    # On crée l'affichage des otpions
    options_print = ""
    for nom, _, _ in graphiques_recommandes:
        options_print += f"{nom}\n"

    choix = utils.show_banner("Graphiques", "Veuillez choisir une option", emplacement="Menu > Graphiques",
                              footer=options_print, frich=True,
                              demande="Entrez votre choix (c pour revenir en arrière): ", alerte=message)

    # Récupérer les choix
    try:
        int_choice = int(choix)
        tup_choix = graphiques_recommandes[int_choice - 1]
        if not tup_choix[1]:
            # On envoie à la consruction de graphiques personnalisés
            composition_graphique(elements)
        else:
            # On envoie les éléments pour la construction du graphique
            compute_graphiques(elements, tup_choix[1], tup_choix[2])
        choix_construction_graphique()
    except (ValueError, IndexError):
        if choix == "c":
            main()
        else:
            choix_construction_graphique("Choix invalide ! (Choix de graphiques)")


def composition_graphique(elements: list):
    """Menu de composition de graphique personnalisé"""

    ordonnes_choisies = []
    abscisse_choisie = None
    message = ""

    # Boucle de demande des paramètres
    while True:
        utils.clear_console()
        utils.show_banner("Graphiques Personnalisés", "Veuillez choisir une option",
                          emplacement="Menu > Graphiques > Graphique Personnalisé")
        rich.print("[red][bold]*[/bold]: Paramètres disponibles uniquement en Abscisses[/red]")
        # On affiche la liste de paramètres
        for index, param in enumerate(elements):
            if not param[1]:
                # Affichage de l'étoile si le paramètre n'est pas autorisé en ordonnée
                rich.print(f"{index + 1}. {param[0]}[red]*[/red]")
            else:
                rich.print(f"{index + 1}. {param[0]}")

        # Affichage du message d'erreur avant celui de la demande
        rich.print(f"[bold][red]{message}[/red][/bold]")

        if len(ordonnes_choisies) == 0:  # Demande des paramètres en ordonnée
            ordonnees = input("Entrez vos paramètres à mettre en ordonnée (Séparés par un espace /!\\ pas plus de 4): ").strip().split(' ')
            if len(ordonnees) == 0:
                message = "Veuillez entrer au moins un paramètre"
            else:
                # Vérificaton pour chaque paramètre entré en ordonnée
                n_o = 0
                for idx_input, inputs_ords_text in enumerate(ordonnees):
                    if n_o < 4:
                        n_o += 1

                        try:
                            # On essaye de convertir en nombre
                            inputs_ords = int(inputs_ords_text)

                            # On vérifie que le paramètre est autorisé en ordonnée
                            if not elements[inputs_ords - 1][1]:
                                message = f"Le paramètre n°{idx_input + 1} n'est pas autorisé en ordonnée"
                                ordonnes_choisies = []
                                break

                            # Si on arrive ici, c'est que tout est bon, on ajoute le paramètre à la liste
                            ordonnes_choisies.append(inputs_ords - 1)
                            message = ""

                        except (ValueError, IndexError):
                            # Si on arrive ici c'est que le paramètre n'est pas valide, on vide la liste et on
                            # recommence
                            message = f"Le paramètre n°{idx_input + 1} n'est pas valide"
                            ordonnes_choisies = []
                            break

        else:  # Demande du paramètre en abscisse
            abscisses = input("Entrez le paramètre à mettre en abscisses: ").strip()

            try:
                # On essaye de convertir l'entrée en nombre
                inputs_abs = int(abscisses)

                # Vérification que le paramètre est dans la liste des paramètres
                _ = elements[inputs_abs - 1][2]

                # Vérification que le paramètre n'est pas déjà en ordonnée
                assert inputs_abs - 1 not in ordonnes_choisies

                # Si on est ici, tout est bon, on sauvegarde le paramètre
                abscisse_choisie = inputs_abs - 1
            except (ValueError, IndexError):  # Erreurs
                message = "Le paramètre entré n'est pas valide"
                abscisse_choisie = None
            except AssertionError:  # Erreurs
                message = "Le paramètre entré est déjà en ordonnée"
                abscisse_choisie = None

        # Si tout à été choisi, on sort de la boucle, sinon on reboucle
        if len(ordonnes_choisies) > 0 and abscisse_choisie is not None:
            break

    # On envoie les éléments pour la construction du graphique
    compute_graphiques(elements, abscisse_choisie, ordonnes_choisies)


def compute_graphiques(elements, abscisse_choisie, ordonnes_choisies):
    """Créer les listes de valeurs des graphiques"""
    # TODO commentaires
    joueurs_df_take = joueurs_df.copy(deep=True)
    if abscisse_choisie == 0:
        msg = ""
        options = "*: tous\ne: Par équipe\ni: Individuellement"
        while True:
            type_select = utils.show_banner("Graphiques Personnalisés",
                                            "Veuillez choisir le mode de selection des joueurs",
                                            footer=options,
                                            demande="Entrez votre choix (c pour revenir en arrière): ",
                                            alerte=msg,
                                            emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                        "joueurs")
            if type_select == "*":
                break
            elif type_select == "e":
                eqs_select = []
                eqs_texte = utils.show_banner("Graphiques Personnalisés",
                                              "Veuillez choisir l(es) équipe(s) des joueurs à afficher",
                                              demande="Entrez vos choix séparés par / (c pour revenir en arrière): ",
                                              emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                          "joueurs")
                for eq_txt in eqs_texte.split('/'):
                    _, res_df = compute_recherche(eq_txt.strip())
                    try:
                        eqs_select.append(res_df.loc[0]["id"])
                    except:
                        pass
                if not eqs_select:
                    msg = "Aucune équipe trouvée"
                else:
                    joueurs_df_take = joueurs_df_take[joueurs_df_take["club"].isin(eqs_select)]
                    break
            elif type_select == "i":
                jrs_select = []
                jrs_texte = utils.show_banner("Graphiques Personnalisés",
                                              "Veuillez choisir les noms des joueurs à afficher",
                                              demande="Entrez vos choix séparés par / (c pour revenir en arrière): ",
                                              emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                          "joueurs")

                for jr_txt in jrs_texte.split('/'):
                    res_df, _ = compute_recherche(jr_txt.strip())
                    try:
                        jrs_select.append(res_df.loc[0]["nom_prenom"])
                    except:
                        pass

                if not jrs_select:
                    msg = "Aucun joueur n'a pu être trouvée"
                else:
                    joueurs_df_take = joueurs_df_take[joueurs_df_take["nom_prenom"].isin(jrs_select)]
                    break
            else:
                msg = "Choix invalide ! (type de selection)"

    print("Préparation de votre graphique")
    utils.show_banner("Graphiques Personnalisés", footer=GRAPH_WAIT,
                      emplacement="Menu > Graphiques > Graphique Personnalisé > Préparation du graphique")

    # En fonction des différents paramètres, il faut parfois faire des moyennes

    if "Club" in elements[abscisse_choisie][0]:  # Si c'est une statistique club
        list_abs = list(clubs_df[elements[abscisse_choisie][3]])
    else:
        if elements[abscisse_choisie][3] in ["poste", "meilleur pied", "date_crea"]:
            list_abs = list(joueurs_df_take[elements[abscisse_choisie][3]].value_counts().index)
        else:
            list_abs = list(joueurs_df_take[elements[abscisse_choisie][3]])

    valeurs = []
    descrs_valeurs = []
    arrondi = 50
    for ord_choisie in ordonnes_choisies:
        # Si c'est une statistique joueur
        if "Club" not in elements[ord_choisie][0]:
            # Si c'est une statistique club
            if "Club" in elements[abscisse_choisie][0]:
                # Calculer la moyenne des statistiques des joueurs pour chaque club
                moyennes = []
                for club in clubs_df[elements[abscisse_choisie][3]]:
                    moyennes.append(
                        round(joueurs_df_take[joueurs_df_take[elements[abscisse_choisie][3] + "_club"] == club][
                                  elements[ord_choisie][3]].mean(), arrondi))
                valeurs.append(moyennes)
                descrs_valeurs.append(elements[ord_choisie][0] + " (Moyenne)")

            else:
                if elements[abscisse_choisie][3] in ["poste", "meilleur pied"]:
                    moyennes = []
                    for elem in list_abs:
                        moyennes.append(round(joueurs_df_take[joueurs_df_take[elements[abscisse_choisie][3]] == elem][
                                                  elements[ord_choisie][3]].mean(), arrondi))

                    valeurs.append(moyennes)
                    descrs_valeurs.append(elements[ord_choisie][0] + " (Moyenne)")

                else:
                    valeurs.append(list(joueurs_df_take[elements[ord_choisie][3]]))
                    descrs_valeurs.append(elements[ord_choisie][0])
        else:
            if "Club" in elements[abscisse_choisie][0]:

                valeurs.append(list(clubs_df[elements[ord_choisie][3]]))
                descrs_valeurs.append(elements[ord_choisie][0])
            else:
                valeurs.append(list(joueurs_df_take[elements[ord_choisie][3] + "_club"]))
                descrs_valeurs.append(elements[ord_choisie][0])

    titre = "Graphique de \""
    for ord_choisie in ordonnes_choisies:
        titre += elements[ord_choisie][0] + ", "
    titre = titre[:-2]
    graphiques_plot(list_abs, valeurs, descrs_valeurs, elements[abscisse_choisie][0], titre + '" en fonction de "' + elements[abscisse_choisie][0] + '"')


def graphiques_plot(list_abs, valeurs, valeurs_decrs, x_legend, title):
    # Liste de couleurs pour les graphiques
    list_colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan", "black",
                   "indigo", "lime", "navy", "teal", "yellow", "aqua", "fuchsia", "maroon", "silver", "white", "violet",
                   "peru"]

    # Pour chaque série de données, on trie les valeurs d'abscisse par ordre croissant
    # Le tout en triant de paire les valeurs d'ordonnées
    for idx_val, val_list in enumerate(valeurs):
        _, valeurs[idx_val] = zip(*sorted(zip(list_abs, val_list), key=lambda e_abs: e_abs[0]))

    list_abs = sorted(list_abs)

    fig, ax = plt.subplots(num="NsiFoot - Graphique")
    # On crée une liste d'axes qui permettent d'avoir différentes unités
    # On prend le nombre de séries de données - 1, car on a déjà un axe par défaut
    axes = [ax] + [ax.twinx() for _ in range(len(valeurs) - 1)]

    if isinstance(list_abs[0], str):  # Graphique en barres
        loc_x = np.arange(len(list_abs))  # Tableau Numpy contenant la localisation des labels
        width = 0.2  # largeur des barres

        ax_del = []
        nombre_index = None
        # Tracer chaque série de données sur son propre axe
        for axe, val, i, legende in zip(axes, valeurs, range(len(valeurs)), valeurs_decrs):
            if "Nombre" in legende:
                if nombre_index is None:
                    nombre_index = i
                    axe.bar(loc_x + (i) * width, val, width, label=legende, color=list_colors[i])
                    axe.set_ylabel(legende)

                else:
                    axes[nombre_index].bar(loc_x + (i) * width, val, width, label=legende, color=list_colors[i])
                    # old_lab = axes[nombre_index].get_ylabel()

                    axes[nombre_index].set_ylabel("Nombre")
                    ax_del.append(i)
            else:
                axe.bar(loc_x + (i) * width, val, width, label=legende, color=list_colors[i])
                axe.set_ylabel(legende)

        # On enlève les axes inutiles
        for idx_del in ax_del:
            axes[idx_del].set_visible(False)

        for idx_del in ax_del:
            try:
                del axes[idx_del]
            except IndexError:
                pass

        # Décalage des différentes échelles pour éviter leur superposition
        for i, axe in enumerate(axes[1:]):
            axe.spines['right'].set_position(('outward', 60 * i))

        # Ajout des légendes en dessous des barres
        ax.set_xticks(loc_x + ((len(valeurs) - 1) * (width / 2)))
        ax.set_xticklabels(list_abs)

    else:  # Courbe + Nuage de points

        # On crée des valeurs pour les courbes de moyenne
        valeurs_moy = []
        list_abs_moy = []
        for index_vals, val_list in enumerate(valeurs):
            moy_temp_vals = {}
            for idx, abs in enumerate(list_abs):
                if abs not in moy_temp_vals:
                    moy_temp_vals[abs] = [val_list[idx]]
                else:
                    moy_temp_vals[abs].append(val_list[idx])
            valeurs_moy.append([])
            list_abs_moy = []
            for k, v in moy_temp_vals.items():
                valeurs_moy[index_vals].append(sum(v) / len(v))
                list_abs_moy.append(k)

        # Tracer chaque série de données sur son propre axe
        ax_del = []
        nombre_index = None
        for axe, val, i, legende in zip(axes, valeurs, range(len(valeurs)), valeurs_decrs):
            # Système permettant de regrouper les axes ayant la même unité (Nombre)
            if "Nombre" in legende:
                if nombre_index is None:
                    nombre_index = i
                    axe.scatter(list_abs, val, label=legende, color=list_colors[i], s=5)
                    axe.set_ylabel(legende)
                else:
                    axes[nombre_index].scatter(list_abs, val, label=legende, color=list_colors[i], s=5)
                    axe.set_ylabel(legende)
                    axes[nombre_index].set_ylabel("Nombre")
                    ax_del.append(i)

            else:
                axe.scatter(list_abs, val, label=legende, color=list_colors[i], s=5)
                axe.set_ylabel(legende)

        # Affichage des courbes de moyenne
        nombre_index = None
        for axe, val_moy, i, legende in zip(axes, valeurs_moy, range(len(valeurs_moy)), valeurs_decrs):
            # Même système permettant de regrouper les axes ayant la même unité (Nombre)
            if "Nombre" in legende:
                if nombre_index is None:
                    nombre_index = i
                    axe.plot(list_abs_moy, val_moy, label=legende + " (Moyenne)", color=list_colors[i])
                else:
                    axes[nombre_index].plot(list_abs_moy, val_moy, label=legende + " (Moyenne)", color=list_colors[i])
                    ax_del.append(i)
            else:
                axe.plot(list_abs_moy, val_moy, label=legende + " (Moyenne)", color=list_colors[i])

        for idx_del in ax_del:
            axes[idx_del].set_visible(False)

        for idx_del in ax_del:
            try:
                del axes[idx_del]
            except IndexError:
                pass

        for i, axe in enumerate(axes[1:]):
            axe.spines['right'].set_position(('outward', 60 * (i)))

    # Ajout des titres et de la légende d'abscisse
    ax.set_xlabel(x_legend)
    ax.set_title(title)

    # On choisit l'endroit de la légende (coin supérieur gauche)
    fig.legend(loc="upper left", bbox_to_anchor=(0, 1), bbox_transform=ax.transAxes)

    # Fonction pour réajuster le graphique en cas de redimensionnement de la fenêtre
    def on_resize(_):
        fig.tight_layout()
        fig.canvas.draw()

    fig.canvas.mpl_connect('resize_event', on_resize)

    # Réajustement du graphique
    plt.tight_layout()

    # Permet de tourner les légendes pour éviter le chevauchement
    plt.gcf().autofmt_xdate()

    # Affichage du graphique

    plt.show()


def rechercher():
    """Menu de recherche de joueur ou d'équipe"""

    # On affiche la décoration et demande la recherche
    recherche = utils.show_banner("Recherche",
                                  "Veuillez rentrer une requête (la forme de la requête n'as pas d'importance)",
                                  emplacement="Menu > Recherche",
                                  demande="Entrez le nom du joueur ou de l'équipe à chercher (c pour revenir en "
                                          "arrière): ")

    # On effectue la recherche
    joueurs_recherche, clubs_recherche = compute_recherche(recherche)
    clubs_recherche.rename(columns={"name": "nom_prenom"}, inplace=True)

    # Affichage des résultats
    # TODO Commentaires

    affichage = "\n"
    found = True
    ecart = 10
    second_df = pd.DataFrame()
    # Afficher en premier le df où il y a le score de ressemblance le plus grand
    if len(joueurs_recherche) == 0 and len(clubs_recherche) == 0:
        found = False
        first_df = pd.DataFrame()
    elif len(joueurs_recherche) == 0:
        first_df = clubs_recherche
    elif len(clubs_recherche) == 0:
        first_df = joueurs_recherche
    else:
        first_df, second_df = (joueurs_recherche, clubs_recherche) if joueurs_recherche.loc[0]["score"] > \
                                                                      clubs_recherche.loc[0]["score"] else (
            clubs_recherche, joueurs_recherche)
        ecart = first_df.loc[0]["score"] - second_df.loc[0]["score"]

    # On ne garde que un seul df si il y a un écart trop important dans laqualité des résultats

    seuil_ecart = 0.1
    if len(first_df) == 1 and (len(second_df) == 0 or ecart > seuil_ecart):
        show_stats(first_df.loc[0])
        rechercher()

    if found:
        ban1, ban2 = ("Joueurs Trouvés", "Equipes Trouvées") if "ville" not in list(first_df.columns) else (
            "Equipes Trouvées", "Joueurs Trouvés")
        max_len_left = 0
        f_list = []
        s_list = []
        for index, row in first_df.iterrows():
            txt = f'{index + 1}. {row["nom_prenom"]}'
            max_len_left = max(max_len_left, len(txt))
            f_list.append(txt)

        max_len_left += 5

        for index, row in second_df.iterrows():
            print(len(f_list) + index + 1)
            txt = f'{len(f_list) + index + 1}. {row["nom_prenom"]}'
            s_list.append(txt)

        if len(f_list) > len(s_list):
            for _ in range(len(f_list) - len(s_list)):
                s_list.append(" ")
        elif len(f_list) < len(s_list):
            for _ in range(len(s_list) - len(f_list)):
                f_list.append(" ")

        if ecart < seuil_ecart:
            affichage += f'{ban1.ljust(max_len_left)}|      {ban2} \n'
            affichage += f'{(len(ban1) * "-").ljust(max_len_left)}|      {len(ban2) * "-"} \n'

            for f_elem, s_elem in zip(f_list, s_list):
                affichage += f'{f_elem.ljust(max_len_left)}|      {s_elem} \n'
        else:
            affichage += f'{ban1}\n'
            affichage += f'{len(ban1) * "-"}\n'
            for f_list_elem in f_list:
                affichage += f'{f_list_elem}\n'
    else:
        affichage = "\nAucun résultat trouvé\n"
        affichage += """
                                                                 
           |--------------|--------------|
           |       ?      |       ?      |
           |--.          .|.          .--|
           [  |    ?    | * |     ?   |  ]
           |--'          `|`          '--|
           |       ?      |       ?      |
           |--------------|--------------|
                                                                             
        """
    message_choix_interne = ""
    while True:
        if not found:
            print(affichage)
            input("Appuyez sur Entrée pour continuer ...")
            break
        rep = utils.show_banner("Résultats Recherche",
                                subtitle=f'"{recherche}"',
                                emplacement="Menu > Recherche > Résultats de la Recherche",
                                footer=affichage,
                                frich=True,
                                alerte=message_choix_interne,
                                demande="Entrez le numéro de l'élément dont vous voulez obtenir les infos. (c pour "
                                        "revenir en arrière): ")

        if rep == "c":
            break
        else:
            try:
                index = int(rep) - 1
                if index < len(first_df):
                    show_stats(first_df.loc[index])
                    break
                else:
                    show_stats(second_df.loc[index - len(first_df)])
                    break
            except ValueError:
                message_choix_interne = "Choix invalide ! (Resultats de recherche)"
    rechercher()


def show_stats(element: pd.Series):
    """Afficher les statistiques d'un joueur ou d'une équipe"""
    # TODO Si joueur, afficher un dessin de terrain avec la position
    console = Console()
    table = Table(title="Statistiques")
    for key, value in element.items():
        table.add_row(str(key), str(value))
    console.print(table)
    element.to_json("club.json")
    input("Suite ?")


def compute_recherche(recherche: str):
    """Permet de rechercher un joueur ou une équipe de façon plutôt efficace"""
    # Seuil de tolérance de ressemblance
    seuil = 0.7
    # On copie les df pour ne pas les modifier
    joueurs_recherche = joueurs_df.copy(deep=True)
    clubs_recherche = clubs_df.copy(deep=True)

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

    # On réduit les df de résultat en gardant les éléments tant qu'il n'y a pas un gros écart de score
    stop = False
    for index, row in joueurs_recherche.iterrows():
        if not stop:
            if index != 0:
                if (joueurs_recherche.iloc[index - 1]["score"] - row["score"] > 0.15 or joueurs_recherche.iloc[0][
                    "score"] - row["score"] > 0.2):
                    joueurs_recherche.drop(index, inplace=True)
                    stop = True
        else:
            joueurs_recherche.drop(index, inplace=True)

    stop = False
    for index, row in clubs_recherche.iterrows():
        if not stop:
            if index != 0 and (
                    clubs_recherche.iloc[index - 1]["score"] - row["score"] > 0.15 or clubs_recherche.iloc[0]["score"] -
                    row["score"] > 0.2):
                clubs_recherche.drop(index, inplace=True)
                stop = True
        else:
            clubs_recherche.drop(index, inplace=True)

    return joueurs_recherche, clubs_recherche


def width_term_guide(re=False):
    """Guide pour l'élargissement du terminal"""
    utils.clear_console()
    w, h = utils.term_size()
    # Verif width
    confort = True
    fonc = True
    if w <= 120:
        confort = False
    if w <= 87:
        fonc = False
    if h <= 33:
        confort = False

    if (not fonc) or (not confort):
        if re:
            if not fonc:
                rich.print("[bold][red]Votre terminal est trop petit pour un affichage fonctionnel[/red][/bold]")
            if not confort:
                rich.print("[red]Votre terminal est trop petit pour un affichage confortable[/red]")
            resp = input("Voulez-vous vraiment continuer ? (o/n): ")
            if resp.lower() == "o":
                return
            else:
                width_term_guide()
        else:
            utils.clear_console()
            print("_")
            rich.print("[green]" + ("#\n" * 33)[:-1] + "~" + "[/green]")
            rich.print("[green]" + "=" * 119 + "[/green]\n")
            rich.print("[red]" + "=" * 86 + "[/red]")

            print("")
            rich.print("[bold]Agrandissez votre terminal pour augmenter l'expérience de navigation[/bold]")
            rich.print(
                "Agrandissez jusqu'a ce que les lignes tiennent complètement sur une ligne (idem pour les colonnes)")
            rich.print("Ligne [red]rouge[/red] : Affichage fonctionnel")
            rich.print("Ligne [green]verte[/green] : Affichage confortable\n")

        input("Appuyez sur Entrée quand vous avez fini ...")
        width_term_guide(True)

    # 120, 35
    # min: 87 cols


if __name__ == "__main__":
    width_term_guide()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Sortie")
