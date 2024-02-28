import matplotlib.pyplot as plt
import numpy as np
import datas
import dessins

import utils
import recherche


# TODO ajouter les relégations etc


def main(message=""):
    """Menu principal"""
    # Afficher le menu principal
    first_choice = utils.show_banner("Menu principal", "Veuillez choisir une option", emplacement="Menu", header=dessins.HEADER,
                                     footer=dessins.MAIN_OPTIONS, demande="Entrez votre choix (Ctrl+C pour quitter): ",
                                     alerte=message)
    # Récupérer les choix
    if first_choice == "1":
        recherche.menu()
    elif first_choice == "2":
        choix_classements()
    elif first_choice == "3":
        choix_construction_graphique()
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


def afficher_classements(df, elem, all=False):
    """Afficher les classements"""

    # Savoir quelle colonne aller chercher pour le nom
    col_name = "name" if "name" in df.columns else "nom_prenom"

    # Obtenir la plus grande largeur de nom_prenom
    max_len = df[col_name].apply(len).max()
    # Remplir la table
    table = ""

    sorted_df = df.sort_values(by=elem[0], ascending=elem[0] in [
                               "rang"]).reset_index(drop=True)
    if all:
        for index, row in sorted_df.iterrows():
            table += f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m{row[elem[0]]}\033[0m\n"
    else:
        for index, row in sorted_df.head(10).iterrows():
            table += f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m{row[elem[0]]}\033[0m\n"
        table += "\n\033[33m...\033[0m\n\n"
        for index, row in sorted_df.tail(10).iterrows():
            table += f"\033[36m{(str(index + 1) + '.').ljust(3)}\033[0m {row[col_name].ljust(max_len)} : \033[96m{row[elem[0]]}\033[0m\n"

    # On affiche la table
    subt = ("Classement des equipes par " if col_name ==
            "name" else "Classement des joueurs par ") + elem[1]
    choix = utils.show_banner("Classement", subt,
                              emplacement="Menu > Classements > Classement",
                              footer=table,
                              demande="Appuyez Entrée pour continuer (* puis Entrée pour tout afficher) :")
    if choix == "*":
        afficher_classements(df, elem, True)


def choix_construction_graphique(message=""):
    """Menu pour choisir entre des graphiques recommandés ou des graphiques personnalisés"""

    # Elements transmis pour les graphiques personnalisés
    # TODO Améliorer les nominations dans les graphiques
    elements = [("Nom du joueur", False, True, "nom_prenom"), ("Poste", False, True, "poste"),
                ("Age", True, True, "age"), ("Poids (en kg)", True, True, "poids"),
                ("Taille (en cm)", True, True, "taille"),
                ("Salaire mensuel (en Millions d'euros)", True, True, "salaire"),
                ("Nombre de buts encaissés", True, True, "buts_e_joueur"),
                ("Nombre de buts Marqués", True, True, "buts_m_joueur"),
                ("Nombre de matchs joués", True, True, "matchs_j"),
                ("Meilleur pied", False, True,
                 "meilleur pied"), ("Nombre de passes décisives", True, True, "pass_d"),
                ("Club", False, True, "name"), ("Rang (Club)", True, True, "rang"),
                ("Nombre de Victoires (Club)", True, True,
                 "victoires"), ("Nombre de Nuls (Club)", True, True, "nuls"),
                ("Nombre de Défaites (Club)", True, True, "defaites"),
                ("Nombre de buts Marqués (Club)", True, True, "buts_m"),
                ("Nombre de buts encaissés (Club)", True, True, "buts_e"),
                ("Date de création du Club", False, True, "date_crea"),
                ("Budget du Club (en Milions d'euros)", True, True, "budget"),
                ("Nombre de titres du Club", True, True, "titres"),
                ("Rendement du club (en fonction du rang et du budget)",
                 True, True, "rendement"),
                ("Domination du club en % d'années titrées", True, True, "domination")]

    # Liste des graphiques recommandés
    # (Nom, Paramètre en abscisse, Paramètres en ordonnée)
    graphiques_recommandes = [("\033[96m1.\033[0m Nombre de buts marqués par club", 11, [16]),
                              (
                                  "\033[96m2.\033[0m Salaire moyen d'un joueur & Nombre de buts moyen marqués en fonction de son poste",
                                  1, [5, 7]),
                              ("\033[96m3.\033[0m Poids des joueurs en fonction de leur taille", 3, [
                               4]),
                              ("\033[96m4.\033[0m Graphiques personnalisés", [], []), ]

    # On crée l'affichage des otpions
    options_print = ""
    for nom, _, _ in graphiques_recommandes:
        options_print += f"{nom}\n"

    choix = utils.show_banner("Graphiques", "Veuillez choisir une option", emplacement="Menu > Graphiques",
                              footer=options_print,
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
            choix_construction_graphique(
                "Choix invalide ! (Choix de graphiques)")


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
        print(
            "\033[1;31m*\033[0;31m: Paramètres disponibles uniquement en Abscisses\033[0m")
        # On affiche la liste de paramètres
        for index, param in enumerate(elements):
            if not param[1]:
                # Affichage de l'étoile si le paramètre n'est pas autorisé en ordonnée
                print(
                    f"\033[96m{index + 1}\033[0m. {param[0]}\033[31m*\033[0m")
            else:
                print(f"\033[96m{index + 1}\033[0m. {param[0]}")

        # Affichage du message d'erreur avant celui de la demande
        print(f"\033[1;31m{message}\033[0m")

        if len(ordonnes_choisies) == 0:  # Demande des paramètres en ordonnée
            ordonnees = input(
                "Entrez vos paramètres à mettre en ordonnée (Séparés par un espace /!\\ pas plus de 4): ").strip().split(
                ' ')
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
            abscisses = input(
                "Entrez le paramètre à mettre en abscisses: ").strip()

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

        # Si tout a été choisi, on sort de la boucle, sinon on reboucle
        if len(ordonnes_choisies) > 0 and abscisse_choisie is not None:
            break

    # On envoie les éléments pour la construction du graphique
    compute_graphiques(elements, abscisse_choisie, ordonnes_choisies)


def compute_graphiques(elements, abscisse_choisie, ordonnes_choisies):
    """Créer les listes de valeurs des graphiques"""
    joueurs_df_take = datas.joueurs_df.copy(deep=True)
    # Si l'abscisse est les noms, on demande à sélectionner les noms
    if abscisse_choisie == 0:
        msg = ""
        # Soit sélectionner tout, soit par équipe, soit par nom de joueur
        options = "*: tous\ne: Par équipe\ni: Individuellement"  # TODO colorer
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
                # On fait une recherche avec les données entrées
                for eq_txt in eqs_texte.split('/'):
                    _, res_df = recherche.compute_recherche(eq_txt.strip())
                    try:
                        eqs_select.append(res_df.loc[0]["id"])
                    except IndexError:
                        pass
                if not eqs_select:
                    msg = "Aucune équipe trouvée"
                else:
                    joueurs_df_take = joueurs_df_take[joueurs_df_take["club"].isin(
                        eqs_select)]
                    break
            elif type_select == "i":
                jrs_select = []
                jrs_texte = utils.show_banner("Graphiques Personnalisés",
                                              "Veuillez choisir les noms des joueurs à afficher",
                                              demande="Entrez vos choix séparés par / (c pour revenir en arrière): ",
                                              emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                          "joueurs")

                # On fait une rechrche avec les données entrées
                for jr_txt in jrs_texte.split('/'):
                    res_df, _ = recherche.compute_recherche(jr_txt.strip())
                    try:
                        jrs_select.append(res_df.loc[0]["nom_prenom"])
                    except:
                        pass

                if not jrs_select:
                    msg = "Aucun joueur n'a pu être trouvée"
                else:
                    joueurs_df_take = joueurs_df_take[joueurs_df_take["nom_prenom"].isin(
                        jrs_select)]
                    break
            elif type_select == "c":
                composition_graphique(elements)
            else:
                msg = "Choix invalide ! (type de selection)"

    print("Préparation de votre graphique")
    utils.show_banner("Graphiques Personnalisés", footer=dessins.GRAPH_WAIT,
                      emplacement="Menu > Graphiques > Graphique Personnalisé > Préparation du graphique")

    # En fonction des différents paramètres, il faut parfois faire des moyennes

    # Définir les valeurs en abscisse
    if "Club" in elements[abscisse_choisie][0]:
        list_abs = list(datas.clubs_df[elements[abscisse_choisie][3]])
    else:
        if elements[abscisse_choisie][3] in ["poste", "meilleur pied", "date_crea"]:
            list_abs = list(
                joueurs_df_take[elements[abscisse_choisie][3]].value_counts().index)
        else:
            list_abs = list(joueurs_df_take[elements[abscisse_choisie][3]])

    valeurs = []
    descrs_valeurs = []
    arrondi = 50
    for ord_choisie in ordonnes_choisies:
        # En fonction du paramètre choisi, il faut faire des moyennes ou pas
        if "Club" not in elements[ord_choisie][0]:
            if "Club" in elements[abscisse_choisie][0]:
                # L'ordonnée s'agit d'une statistique joueur et l'abscisse d'une statistique club
                # Calculer la moyenne des statistiques des joueurs pour chaque club
                moyennes = []
                for club in datas.clubs_df[elements[abscisse_choisie][3]]:
                    moyennes.append(
                        round(joueurs_df_take[joueurs_df_take[elements[abscisse_choisie][3] + "_club"] == club][
                            elements[ord_choisie][3]].mean(), arrondi))
                valeurs.append(moyennes)
                descrs_valeurs.append(elements[ord_choisie][0] + " (Moyenne)")

            else:
                # L'ordonnée s'agit d'une statistique joueur et l'abscisse d'une statistique joueur
                # Pas de moyenne à calculer sauf si on a affaire au poste ou au meilleur pied
                if elements[abscisse_choisie][3] in ["poste", "meilleur pied"]:
                    moyennes = []
                    for elem in list_abs:
                        moyennes.append(round(joueurs_df_take[joueurs_df_take[elements[abscisse_choisie][3]] == elem][
                            elements[ord_choisie][3]].mean(), arrondi))

                    valeurs.append(moyennes)
                    descrs_valeurs.append(
                        elements[ord_choisie][0] + " (Moyenne)")

                else:
                    valeurs.append(
                        list(joueurs_df_take[elements[ord_choisie][3]]))
                    descrs_valeurs.append(elements[ord_choisie][0])
        else:
            if "Club" in elements[abscisse_choisie][0]:
                # L'ordonnée s'agit d'une statistique club et l'abscisse d'une statistique club → Pas de moyenne
                valeurs.append(list(datas.clubs_df[elements[ord_choisie][3]]))
                descrs_valeurs.append(elements[ord_choisie][0])
            else:
                # L'ordonnée s'agit d'une statistique club et l'abscisse d'une statistique joueur => Pas de moyenne
                valeurs.append(
                    list(joueurs_df_take[elements[ord_choisie][3] + "_club"]))
                descrs_valeurs.append(elements[ord_choisie][0])

    # On crée un titre de graphique
    titre = "Graphique de \""
    for ord_choisie in ordonnes_choisies:
        titre += elements[ord_choisie][0] + ", "
    titre = titre[:-2]
    graphiques_plot(list_abs, valeurs, descrs_valeurs, elements[abscisse_choisie][0],
                    titre + '" en fonction de "' + elements[abscisse_choisie][0] + '"')


def graphiques_plot(list_abs, valeurs, valeurs_decrs, x_legend, title):
    # Liste de couleurs pour les graphiques
    list_colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan", "black",
                   "indigo", "lime", "navy", "teal", "yellow", "aqua", "fuchsia", "maroon", "silver", "white", "violet",
                   "peru"]

    # Pour chaque série de données, on trie les valeurs d'abscisse par ordre croissant
    # Le tout en triant de paire les valeurs d'ordonnées
    for idx_val, val_list in enumerate(valeurs):
        _, valeurs[idx_val] = zip(
            *sorted(zip(list_abs, val_list), key=lambda e_abs: e_abs[0]))

    list_abs = sorted(list_abs)

    fig, ax = plt.subplots(num="NsiFoot - Graphique")
    # On crée une liste d'axes qui permettent d'avoir différentes unités
    # On prend le nombre de séries de données - 1, car on a déjà un axe par défaut
    axes = [ax] + [ax.twinx() for _ in range(len(valeurs) - 1)]

    if isinstance(list_abs[0], str):  # Graphique en barres
        # Tableau Numpy contenant la localisation des labels
        loc_x = np.arange(len(list_abs))
        width = 0.2  # largeur des barres

        ax_del = []
        nombre_index = None
        # Tracer chaque série de données sur son propre axe
        for axe, val, i, legende in zip(axes, valeurs, range(len(valeurs)), valeurs_decrs):
            if "Nombre" in legende:
                if nombre_index is None:
                    nombre_index = i
                    axe.bar(loc_x + (i) * width, val, width,
                            label=legende, color=list_colors[i])
                    axe.set_ylabel(legende)

                else:
                    axes[nombre_index].bar(
                        loc_x + i * width, val, width, label=legende, color=list_colors[i])
                    axes[nombre_index].set_ylabel("Nombre")
                    ax_del.append(i)
            else:
                axe.bar(loc_x + (i) * width, val, width,
                        label=legende, color=list_colors[i])
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
                    axe.scatter(list_abs, val, label=legende,
                                color=list_colors[i], s=5)
                    axe.set_ylabel(legende)
                else:
                    axes[nombre_index].scatter(
                        list_abs, val, label=legende, color=list_colors[i], s=5)
                    axe.set_ylabel(legende)
                    axes[nombre_index].set_ylabel("Nombre")
                    ax_del.append(i)

            else:
                axe.scatter(list_abs, val, label=legende,
                            color=list_colors[i], s=5)
                axe.set_ylabel(legende)

        # Affichage des courbes de moyenne
        nombre_index = None
        for axe, val_moy, i, legende in zip(axes, valeurs_moy, range(len(valeurs_moy)), valeurs_decrs):
            # Même système permettant de regrouper les axes ayant la même unité (Nombre)
            if "Nombre" in legende:
                if nombre_index is None:
                    nombre_index = i
                    axe.plot(list_abs_moy, val_moy, label=legende +
                             " (Moyenne)", color=list_colors[i])
                else:
                    axes[nombre_index].plot(
                        list_abs_moy, val_moy, label=legende + " (Moyenne)", color=list_colors[i])
                    ax_del.append(i)
            else:
                axe.plot(list_abs_moy, val_moy, label=legende +
                         " (Moyenne)", color=list_colors[i])

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
    fig.legend(loc="upper left", bbox_to_anchor=(
        0, 1), bbox_transform=ax.transAxes)

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
                print(
                    "\033[1;31mVotre terminal est trop petit pour un affichage fonctionnel\033[0m")
            if not confort:
                print(
                    "\033[31mVotre terminal est trop petit pour un affichage confortable\033[0m")
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

    # 120, 35
    # min: 87 cols


if __name__ == "__main__":
    # width_term_guide()
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("Sortie")
