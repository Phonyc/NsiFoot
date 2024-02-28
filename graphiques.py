"""Module de graphiques"""
import matplotlib.pyplot as plt
import numpy as np

import datas
import dessins
import utils
from recherche import compute_recherche


def menu(message=""):
    """Menu pour choisir entre des graphiques recommandés ou des graphiques personnalisés"""

    # On crée l'affichage des options
    options_print = ""
    for nom, _, _ in datas.GRAPH_REC[:-1]:
        options_print += f"{nom}\n"
    options_print += "\n" + datas.GRAPH_REC[-1][0]

    choix = utils.show_page("Graphiques", "Veuillez choisir une option", emplacement="Menu > Graphiques",
                            footer=options_print,
                            demande="Entrez votre choix (c pour revenir en arrière): ", alerte=message)

    # Récupérer les choix
    try:
        int_choice = int(choix)
        tup_choix = datas.GRAPH_REC[int_choice - 1]
        if not tup_choix[1]:
            # On envoie à la construction de graphiques personnalisés
            menu_composition_graphique()
        else:
            # On envoie les éléments pour la construction du graphique
            compute_graphiques(tup_choix[1], tup_choix[2])
        menu()
    except (ValueError, IndexError):
        if choix == "c":
            return
        else:
            menu(
                "Choix invalide ! (Choix de graphiques)")


def menu_composition_graphique():
    """Menu de composition de graphique personnalisé"""

    ordonnes_choisies = compo_graphiques_ask_ords()
    if not ordonnes_choisies:
        return

    abscisse_choisie = compo_graphiques_ask_abs(ordonnes_choisies)

    if abscisse_choisie is None:
        return

    # On envoie les éléments pour la construction du graphique
    compute_graphiques(abscisse_choisie, ordonnes_choisies)


def compo_graphiques_ask_ords():
    """Demande des paramètres en ordonnée pour la composition de graphiques"""
    message = ""
    ordonnes_choisies = []
    while True:
        # Demande des paramètres en ordonnée
        compo_graphiques_show_liste(message)
        ordonnees_input = input("Entrez vos paramètres à mettre en ordonnée (Séparés par un espace /!\\ pas plus de "
                                "4) (c pour sortir): ").strip()
        if ordonnees_input == "c":
            return []

        ordonnees_input_list = ordonnees_input.split(' ')
        if len(ordonnees_input_list) == 0:
            message = "Veuillez entrer au moins un paramètre"
        elif len(ordonnees_input_list) > 4:
            message = "Veuillez entrer moins de 4 paramètres"
        else:
            # Vérification pour chaque paramètre entré en ordonnée
            for idx_input, inputs_ords_text in enumerate(ordonnees_input_list):
                try:
                    # On essaye de convertir en nombre
                    inputs_ords = int(inputs_ords_text)

                    # On vérifie que le paramètre est autorisé en ordonnée
                    if not datas.GRAPH_ELEMENTS[inputs_ords - 1][1]:
                        message = f"Le paramètre n°{idx_input + 1} n'est pas autorisé en ordonnée"
                        ordonnes_choisies = []
                        break

                    # Si on arrive ici, c'est que tout est bon, on ajoute le paramètre à la liste
                    ordonnes_choisies.append(inputs_ords - 1)
                    message = ""

                except (ValueError, IndexError):
                    # Si on arrive ici, c'est que le paramètre n'est pas valide, on vide la liste et on
                    # recommence
                    message = f"Le paramètre n°{idx_input + 1} n'est pas valide"
                    ordonnes_choisies = []
                    break
        if len(ordonnes_choisies) > 0:
            break

    return ordonnes_choisies


def compo_graphiques_ask_abs(ordonnes_choisies):
    """Demande du paramètre en abscisse pour la composition de graphiques"""
    message = ""
    while True:
        # Demande du paramètre en abscisse
        compo_graphiques_show_liste(message)
        abscisses = input(
            "Entrez le paramètre à mettre en abscisses (c pour sortir): ").strip()
        if abscisses == "c":
            return None
        try:
            # On essaye de convertir l'entrée en nombre
            inputs_abs = int(abscisses)

            # Vérification que le paramètre est dans la liste des paramètres
            _ = datas.GRAPH_ELEMENTS[inputs_abs - 1][2]

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
        if abscisse_choisie is not None:
            break
    return abscisse_choisie


def compo_graphiques_show_liste(message=""):
    """Affiche la liste des paramètres pour la composition de graphiques personnalisés"""
    utils.clear_console()
    utils.show_page("Graphiques Personnalisés", "Veuillez choisir une option",
                    emplacement="Menu > Graphiques > Graphique Personnalisé")
    print(
        "\033[1;31m*\033[0;31m: Paramètres disponibles uniquement en Abscisses\033[0m")
    # On affiche la liste de paramètres
    for index, param in enumerate(datas.GRAPH_ELEMENTS):
        if not param[1]:
            # Affichage de l'étoile si le paramètre n'est pas autorisé en ordonnée
            print(
                f"\033[96m{index + 1}\033[0m. {param[0]}\033[31m*\033[0m")
        else:
            print(f"\033[96m{index + 1}\033[0m. {param[0]}")

    # Affichage du message d'erreur avant celui de la demande
    print(f"\033[1;31m{message}\033[0m")


def compute_graphiques(abscisse_choisie, ordonnes_choisies):
    """Créer les listes de valeurs des graphiques"""
    joueurs_df_take = datas.joueurs_df.copy(deep=True)
    # Si l'abscisse est les noms, on demande à sélectionner les noms
    if abscisse_choisie == 0:
        joueurs_df_take = select_joueurs(joueurs_df_take)
    print("Préparation de votre graphique")
    utils.show_page("Graphiques Personnalisés", footer=dessins.GRAPH_WAIT,
                    emplacement="Menu > Graphiques > Graphique Personnalisé > Préparation du graphique")

    # Définir les valeurs en abscisse
    if "Club" in datas.GRAPH_ELEMENTS[abscisse_choisie][0]:
        list_abs = list(datas.clubs_df[datas.GRAPH_ELEMENTS[abscisse_choisie][3]])
    else:
        if datas.GRAPH_ELEMENTS[abscisse_choisie][3] in ["poste", "meilleur pied", "date_crea"]:
            list_abs = list(
                joueurs_df_take[datas.GRAPH_ELEMENTS[abscisse_choisie][3]].value_counts().index)
        else:
            list_abs = list(joueurs_df_take[datas.GRAPH_ELEMENTS[abscisse_choisie][3]])

    # En fonction du paramètre choisi, il faut faire des moyennes ou pas
    # Faire des moyennes en fonction des paramètres choisis
    valeurs = []
    descrs_valeurs = []
    arrondi = 50
    for ord_choisie in ordonnes_choisies:
        if "Club" not in datas.GRAPH_ELEMENTS[ord_choisie][0]:
            if "Club" in datas.GRAPH_ELEMENTS[abscisse_choisie][0]:
                # L'ordonnée s'agit d'une statistique joueur et l'abscisse d'une statistique club
                # Calculer la moyenne des statistiques des joueurs pour chaque club
                moyennes = []
                for club in datas.clubs_df[datas.GRAPH_ELEMENTS[abscisse_choisie][3]]:
                    moyennes.append(
                        round(joueurs_df_take[
                                  joueurs_df_take[datas.GRAPH_ELEMENTS[abscisse_choisie][3] + "_club"] == club][
                                  datas.GRAPH_ELEMENTS[ord_choisie][3]].mean(), arrondi))
                valeurs.append(moyennes)
                descrs_valeurs.append(datas.GRAPH_ELEMENTS[ord_choisie][0] + " (Moyenne)")

            else:
                # L'ordonnée s'agit d'une statistique joueur et l'abscisse d'une statistique joueur
                # Pas de moyenne à calculer sauf si on a affaire au poste ou au meilleur pied
                if datas.GRAPH_ELEMENTS[abscisse_choisie][3] in ["poste", "meilleur pied"]:
                    moyennes = []
                    for elem in list_abs:
                        moyennes.append(
                            round(joueurs_df_take[joueurs_df_take[datas.GRAPH_ELEMENTS[abscisse_choisie][3]] == elem][
                                      datas.GRAPH_ELEMENTS[ord_choisie][3]].mean(), arrondi))

                    valeurs.append(moyennes)
                    descrs_valeurs.append(
                        datas.GRAPH_ELEMENTS[ord_choisie][0] + " (Moyenne)")

                else:
                    valeurs.append(
                        list(joueurs_df_take[datas.GRAPH_ELEMENTS[ord_choisie][3]]))
                    descrs_valeurs.append(datas.GRAPH_ELEMENTS[ord_choisie][0])
        else:
            if "Club" in datas.GRAPH_ELEMENTS[abscisse_choisie][0]:
                # L'ordonnée s'agit d'une statistique club et l'abscisse d'une statistique club → Pas de moyenne
                valeurs.append(list(datas.clubs_df[datas.GRAPH_ELEMENTS[ord_choisie][3]]))
                descrs_valeurs.append(datas.GRAPH_ELEMENTS[ord_choisie][0])
            else:
                # L'ordonnée s'agit d'une statistique club et l'abscisse d'une statistique joueur → Pas de moyenne
                valeurs.append(
                    list(joueurs_df_take[datas.GRAPH_ELEMENTS[ord_choisie][3] + "_club"]))
                descrs_valeurs.append(datas.GRAPH_ELEMENTS[ord_choisie][0])

    # On crée un titre de graphique
    titre = "Graphique de \""
    for ord_choisie in ordonnes_choisies:
        titre += datas.GRAPH_ELEMENTS[ord_choisie][0] + ", "
    titre = titre[:-2]
    graphiques_plot(list_abs, valeurs, descrs_valeurs, datas.GRAPH_ELEMENTS[abscisse_choisie][0],
                    titre + '" en fonction de "' + datas.GRAPH_ELEMENTS[abscisse_choisie][0] + '"')


def select_joueurs(joueurs_df_take):
    """Sélection des joueurs pour le graphique"""
    msg = ""
    # Soit sélectionner tout, soit par équipe, soit par nom de joueur
    options = "\033[96m*\033[0m: tous\n\033[96me\033[0m: Par équipe\n\033[96mi\033[0m: Individuellement"
    while True:
        type_select = utils.show_page("Graphiques Personnalisés",
                                      "Veuillez choisir le mode de selection des joueurs",
                                      footer=options,
                                      demande="Entrez votre choix (c pour revenir en arrière): ",
                                      alerte=msg,
                                      emplacement="Menu > Graphiques > Graphique Personnalisé > Selection joueurs")
        if type_select == "*":
            break
        elif type_select == "e":
            # Selection par equipe
            eqs_select = []
            eqs_texte = utils.show_page("Graphiques Personnalisés",
                                        "Veuillez choisir l(es) équipe(s) des joueurs à afficher",
                                        demande="Entrez vos choix séparés par / (c pour revenir en arrière): ",
                                        emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                    "joueurs")
            # On fait une recherche avec les données entrées
            for eq_txt in eqs_texte.split('/'):
                _, res_df = compute_recherche(eq_txt.strip())
                try:
                    eqs_select.append(res_df.loc[0]["id"])
                except (IndexError, KeyError):
                    pass
            if not eqs_select:
                msg = "Aucune équipe trouvée"
            else:
                joueurs_df_take = joueurs_df_take[joueurs_df_take["club"].isin(
                    eqs_select)]
                break

        elif type_select == "i":
            # Selection par joueurs
            jrs_select = []
            jrs_texte = utils.show_page("Graphiques Personnalisés",
                                        "Veuillez choisir les noms des joueurs à afficher",
                                        demande="Entrez vos choix séparés par / (c pour revenir en arrière): ",
                                        emplacement="Menu > Graphiques > Graphique Personnalisé > Selection des "
                                                    "joueurs")

            # On fait une recherche avec les données entrées
            for jr_txt in jrs_texte.split('/'):
                res_df, _ = compute_recherche(jr_txt.strip())
                try:
                    jrs_select.append(res_df.loc[0]["nom_prenom"])
                except (IndexError, KeyError):
                    pass

            if not jrs_select:
                msg = "Aucun joueur n'a pu être trouvée"
            else:
                joueurs_df_take = joueurs_df_take[joueurs_df_take["nom_prenom"].isin(
                    jrs_select)]
                break
        elif type_select == "c":
            # Retour
            menu_composition_graphique()
        else:
            msg = "Choix invalide ! (type de selection)"

    return joueurs_df_take


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
                    axe.bar(loc_x + i * width, val, width,
                            label=legende, color=list_colors[i])
                    axe.set_ylabel(legende)

                else:
                    axes[nombre_index].bar(
                        loc_x + i * width, val, width, label=legende, color=list_colors[i])
                    axes[nombre_index].set_ylabel("Nombre")
                    ax_del.append(i)
            else:
                axe.bar(loc_x + i * width, val, width,
                        label=legende, color=list_colors[i])
                axe.set_ylabel(legende)

        # Ajout des légendes en dessous des barres
        ax.set_xticks(loc_x + ((len(valeurs) - 1) * (width / 2)))
        ax.set_xticklabels(list_abs)

    else:  # Courbe + Nuage de points

        # On crée des valeurs pour les courbes de moyenne
        valeurs_moy = []
        list_abs_moy = []
        for index_vals, val_list in enumerate(valeurs):
            moy_temp_vals = {}
            for idx, abscisse in enumerate(list_abs):
                if abscisse not in moy_temp_vals:
                    moy_temp_vals[abscisse] = [val_list[idx]]
                else:
                    moy_temp_vals[abscisse].append(val_list[idx])
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

    # Supprimer / Cacher les axes inutiles
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

    # Ajout des titres et de la légende d'abscisse
    ax.set_xlabel(x_legend)
    ax.set_title(title)

    # On choisit l'endroit de la légende (coin supérieur gauche)
    fig.legend(loc="upper left", bbox_to_anchor=(
        0, 1), bbox_transform=ax.transAxes)

    # Fonction pour réajuster le graphique en cas de redimensionnement de la fenêtre
    def on_resize(_):
        """Réajuster tout quand la fenêtre est redimensionnée"""
        fig.tight_layout()
        fig.canvas.draw()

    fig.canvas.mpl_connect('resize_event', on_resize)

    # Réajustement du graphique
    plt.tight_layout()

    # Permet de tourner les légendes pour éviter le chevauchement
    plt.gcf().autofmt_xdate()

    # Affichage du graphique

    plt.show()
