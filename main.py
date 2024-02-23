import matplotlib.pyplot as plt
import numpy as np
import pandas
import pandas as pd
from rich import print
import utils
from rich.console import Console
from rich.table import Table
import datetime

#  TODO Interface, ajouter des clear console etc
# Charger les données des fichiers CSV
clubs_df = pd.read_csv("clubs.csv", delimiter=';')
clubs_df[["date_crea"]] = clubs_df[["date_crea"]].astype(str)
joueurs_df = pd.read_csv("joueurs.csv", delimiter=';')
# joueurs_df.columns = [col + "_joueur" for col in joueurs_df.columns]
col_origin = list(joueurs_df.columns)
joueurs_df = pd.merge(joueurs_df, clubs_df, left_on='club',
                      right_on='id', how='left', suffixes=('_joueur', '_club'))
cols_nw = list(joueurs_df.columns)
for col in cols_nw:
    if col not in col_origin:
        if not col.endswith("_club"):
            if not col.endswith("_joueur"):
                joueurs_df.rename(columns={col: col + "_club"}, inplace=True)
# On prend 2023 étant donné que l'on possède les données pour la saison 2022-2023
joueurs_df.insert(0, "age", joueurs_df.apply(
    lambda jx: 2023 - int(jx["birthdate"][:4]), axis=1))
joueurs_df.insert(0, "nom_prenom", joueurs_df.apply(
    lambda jx: f"{jx['nom']} {jx['prenom']}", axis=1))
joueurs_df.sort_values(by="nom_prenom", inplace=True)
joueurs_df.reset_index(drop=True, inplace=True)

def main():
    """Menu principal"""
    print("""[bold]Menu principal[/bold]
        1. Rechercher un joueur ou une équipe
        2. Afficher un classement
        3. Afficher des graphiques avec Matplotlib""")
    first_choice = input("Entrez votre choix : ")
    if first_choice == "1":
        rechercher()
    elif first_choice == "2":
        afficher_classements()
    elif first_choice == "3":
        choix_graphiques()
    else:
        print("Choix invalide. Veuillez réessayer.")


def afficher_classements():
    """Afficher les classements"""
    print("classements")

def choix_graphiques():
    elements = [
        ("Nom du joueur", False, True, "nom_prenom"),
        ("Poste", False, True, "poste"),
        ("Age", True, True, "age"),
        ("Poids (en kg)", True, True, "poids"),
        ("Taille (en cm)", True, True, "taille"),
        ("Salaire mensuel (en Millions d'euros)", True, True, "salaire"),
        ("Buts encaissés", True, True, "buts_e_joueur"),
        ("Buts Marqués", True, True, "buts_m_joueur"),
        ("Nombre de matchs joués", True, True, "matchs_j"),
        ("Meilleur pied", False, True, "meilleur pied"),
        ("Nombre de passes décisives", True, True, "pass_d"),
        ("Club", False, True, "name"),
        ("Rang (Club)", True, True, "rang"),
        ("Nombre de Victoires (Club)", True, True, "victoires"),
        ("Nombre de Nuls (Club)", True, True, "nuls"),
        ("Nombre de défaites (Club)", True, True, "defaites"),
        ("Buts Marqués (Club)", True, True, "buts_m"),
        ("Buts encaissés (Club)", True, True, "buts_e"),
        ("Date de création du Club", False, True, "date_crea"),
        ("Budget du Club (en Milions d'euros)", True, True, "budget"),
        ("Nombre de titres du Club", True, True, "titres"),
    ]

    ordonnes_choisies = []
    abscisse_choisie = None
    message = ""
    while True:
        # TODO clear console
        print("Choisissez vos paramètres")
        print("[red][bold]*[/bold]: Paramètres disponibles uniquement en Abscisses[/red]")
        for index, param in enumerate(elements):
            if not param[1]:
                print(f"{index + 1}. {param[0]}[red]*[/red]")
            else:
                print(f"{index + 1}. {param[0]}")
        print(f"[bold][red]{message}[/red][/bold]")
        if len(ordonnes_choisies) == 0:
            ordonnees = input("Entrez vos paramètres à mettre en ordonnée (Séparés par un espace): ").strip().split(' ')
            if len(ordonnees) == 0:
                message = "Veuillez entrer au moins un paramètre"
            else:
                for idx_input, inputs_ords_text in enumerate(ordonnees):
                    try:
                        inputs_ords = int(inputs_ords_text)
                        if not elements[inputs_ords - 1][1]:
                            message = f"Le paramètre n°{idx_input + 1} n'est pas autorisé en ordonnée"
                            ordonnes_choisies = []
                            break
                        ordonnes_choisies.append(inputs_ords - 1)
                        message = ""
                    except (ValueError, IndexError):
                        message = f"Le paramètre n°{idx_input + 1} n'est pas valide"
                        ordonnes_choisies = []
                        break
        else:
            abscisses = input("Entrez le paramètre à mettre en abscisses: ").strip()

            try:
                inputs_abs = int(abscisses)
                _ = elements[inputs_abs - 1][2]
                assert inputs_abs - 1 not in ordonnes_choisies
                abscisse_choisie = inputs_abs - 1
            except (ValueError, IndexError):
                message = "Le paramètre entré n'est pas valide"
                abscisse_choisie = None
            except AssertionError:
                message = "Le paramètre entré est déjà en ordonnée"
                abscisse_choisie = None

        if len(ordonnes_choisies) > 0 and abscisse_choisie is not None:
            break

    
    
    if "Club" in elements[abscisse_choisie][0]: # Si c'est une statistique club
        list_abs = list(clubs_df[elements[abscisse_choisie][3]])
    else:
        if elements[abscisse_choisie][3] in ["poste", "meilleur pied", "date_crea"]:
            list_abs = list(joueurs_df[elements[abscisse_choisie][3]].value_counts().index)
        else:
            list_abs = list(joueurs_df[elements[abscisse_choisie][3]])
            print(list_abs)


    valeurs = []
    descrs_valeurs = []
    arrondi = 50
    for ord_choisie in ordonnes_choisies:
        if "Club" not in elements[ord_choisie][0]: # Si c'est une statistique joueur
            if "Club" in elements[abscisse_choisie][0]: # Si c'est une statistique club
                # Calculer la moyenne des statistiques des joueurs pour chaque club
                moyennes = []
                for club in clubs_df[elements[abscisse_choisie][3]]:
                    moyennes.append(round(joueurs_df[joueurs_df[elements[abscisse_choisie][3] + "_club"] == club][elements[ord_choisie][3]].mean(), arrondi))
                valeurs.append(moyennes)
                descrs_valeurs.append(elements[ord_choisie][0] + " (Moyenne)")
            
            else:
                # TODO Condition pour sélectionner les joueurs
                if elements[abscisse_choisie][3] in ["poste", "meilleur pied"]:
                    moyennes = []
                    for elem in list_abs:
                        moyennes.append(round(joueurs_df[joueurs_df[elements[abscisse_choisie][3]] == elem][elements[ord_choisie][3]].mean(), arrondi))

                    valeurs.append(moyennes)
                    descrs_valeurs.append(elements[ord_choisie][0] + " (Moyenne)")
               
                else:
                    valeurs.append(list(joueurs_df[elements[ord_choisie][3]]))
                    descrs_valeurs.append(elements[ord_choisie][0])
        else:
            if "Club" in elements[abscisse_choisie][0]:

                valeurs.append(list(clubs_df[elements[ord_choisie][3]]))
                descrs_valeurs.append(elements[ord_choisie][0])
            else:
                valeurs.append(list(joueurs_df[elements[ord_choisie][3] + "_club"]))
                descrs_valeurs.append(elements[ord_choisie][0])

    
    graphiques_plot(list_abs, valeurs, descrs_valeurs, elements[abscisse_choisie][0], "Mon Titre")    


def graphiques_plot(list_abs, valeurs, valeurs_decrs, x_legend, title):
    if type(list_abs[0]) == str:
        plot_barres(list_abs, valeurs, valeurs_decrs, x_legend, title)
    else:
        plot_scatter(list_abs, valeurs, valeurs_decrs, x_legend, title)      

def plot_barres(list_abs, valeurs, valeurs_decrs, x_legend, title):
    for idx_val, val_list in enumerate(valeurs):
        _, valeurs[idx_val] = zip(*sorted(zip(list_abs, val_list), key=lambda x: x[0]))
    list_abs = sorted(list_abs)
    x = np.arange(len(list_abs)) # localisation des labels
    width = 0.2  # largeur des barres

    fig, ax = plt.subplots()

    # Créer un axe pour chaque série de données
    axes = [ax] + [ax.twinx() for _ in range(len(valeurs) - 1)]

    # Décaler les axes pour éviter la superposition
    for i, axe in enumerate(axes[2:], 2):
        axe.spines['right'].set_position(('outward', 60 * (i - 1)))

    list_colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"]
    # Tracer chaque série de données sur son propre axe
    ct = 0
    for axe, val, i, legende in zip(axes, valeurs, range(len(valeurs)), valeurs_decrs):
        axe.bar(x + (i) * width, val, width, label=legende, color=list_colors[i])
        axe.set_ylabel(legende)
        ct += 1

    # Ajout des labels, titre et légende
    ax.set_xlabel(x_legend)
    ax.set_title(title)
    ax.set_xticks(x + ((ct - 1) * width / 2))
    ax.set_xticklabels(list_abs)

    fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
    def on_resize(_):
        fig.tight_layout()
        fig.canvas.draw()
    _ = fig.canvas.mpl_connect('resize_event', on_resize)
    plt.tight_layout()

    plt.gcf().autofmt_xdate()
    plt.show()
    
def plot_scatter(list_abs, valeurs, valeurs_decrs, x_legend, title):
    
    for idx_val, val_list in enumerate(valeurs):
        _, valeurs[idx_val] = zip(*sorted(zip(list_abs, val_list), key=lambda x: x[0]))
    list_abs = sorted(list_abs)

    valeurs_moy = []
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

    fig, ax = plt.subplots()

    # Créer un axe pour chaque série de données
    axes = [ax] + [ax.twinx() for _ in range(len(valeurs) - 1)]

    # Décaler les axes pour éviter la superposition
    for i, axe in enumerate(axes[2:], 2):
        axe.spines['right'].set_position(('outward', 60 * (i - 1)))

    list_colors = ["blue", "orange", "green", "red", "purple", "brown", "pink", "gray", "olive", "cyan"] * 2
    # Tracer chaque série de données sur son propre axe
    
    for axe, val, i, legende in zip(axes, valeurs, range(len(valeurs)), valeurs_decrs):
        axe.scatter(list_abs, val, label=legende, color=list_colors[i], s=5)
        axe.set_ylabel(legende)
    for axe, val_moy, i, legende in zip(axes, valeurs_moy, range(len(valeurs_moy)), valeurs_decrs):

        axe.plot(list_abs_moy, val_moy, label=legende + " (Moyenne)", color=list_colors[i])

    # Ajout des labels, titre et légende
    ax.set_xlabel(x_legend)
    ax.set_title(title)

    fig.legend(loc="upper left", bbox_to_anchor=(0,1), bbox_transform=ax.transAxes)
    
    def on_resize(_):
        fig.tight_layout()
        fig.canvas.draw()
    _ = fig.canvas.mpl_connect('resize_event', on_resize)
    plt.tight_layout()

    
    plt.gcf().autofmt_xdate()
    plt.show()
   

def rechercher():
    """Rechercher un joueur ou une équipe"""
    print("""
+-----------+
| Recherche |
+-----------+""")
    recherche = input("Entrez le nom du joueur ou de l'équipe : ").strip()
    joueurs_recherche, clubs_recherche = compute_recherche(recherche)
    # Affichage des résultats
    # TODO Si la différence entre le max score des équipes et des joueurs est trop grande, on donne que le plus grand
    # S'il y a 1 seul résultat dans 1 seul df gardé, on prend le résultat
    #  Sinon on affiche une liste et on demande à l'utilisateur de choisir

    text_1 = ""
    act_ind = 1
    for index, row in joueurs_recherche.iterrows():
        text_1 += f"{index + 1}. {row['nom']} {row['prenom']}\n"
        act_ind += 1
    text_2 = ""
    for index, row in clubs_recherche.iterrows():
        text_2 += f"{index + act_ind}. {row['name']}\n"
    # Afficher un titre encadré

    print("""
+------------------+
| Equipes trouvées |
+------------------+""")

    print(text_2)

    print("""
+-------------------+
|  Joueurs trouvés  |
+-------------------+""")

    print(text_1)

    while True:
        choix = input(
            "Entrez le numéro du joueur ou de l'équipe pour plus d'informations (0: Sortir): ")
        try:
            choix = int(choix)
            if choix == 0:
                break
            if choix in range(1, act_ind):
                show_stats(joueurs_recherche.iloc[choix - 1], "joueur")
                break
            elif choix in range(act_ind, act_ind + len(clubs_recherche)):
                show_stats(clubs_recherche.iloc[choix - act_ind], "club")
                break
            else:
                print("Choix invalide.")
        except ValueError:
            print("Choix invalide.")


def show_stats(element: pandas.Series, type: str):
    """Afficher les statistiques d'un joueur ou d'une équipe"""
    console = Console()
    table = Table(title="Statistiques")
    for key, value in element.items():
        table.add_row(str(key), str(value))
    console.print(table)


def compute_recherche(recherche: str):
    seuil = 0.7
    joueurs_recherche = joueurs_df.copy(deep=True)
    clubs_recherche = clubs_df.copy(deep=True)
    if " " in recherche:
        joueurs_recherche.insert(0, "nom_prenom_score",
                                 joueurs_df.apply(lambda x: utils.similar(f'{x["nom"]} {x["prenom"]}', recherche),
                                                  axis=1))
        joueurs_recherche.insert(0, "prenom_nom_score",
                                 joueurs_df.apply(lambda x: utils.similar(f'{x["prenom"]} {x["nom"]}', recherche),
                                                  axis=1))
        joueurs_recherche = joueurs_recherche[
            (joueurs_recherche['prenom_nom_score'] > seuil) | (joueurs_recherche['nom_prenom_score'] > seuil)]
        joueurs_recherche.insert(0, "score", joueurs_recherche.apply(
            lambda row: max(row["nom_prenom_score"], row["prenom_nom_score"]), axis=1))

    else:

        joueurs_recherche.insert(0, "nom_score",
                                 joueurs_df.apply(lambda x: utils.similar(f'{x["nom"]}', recherche), axis=1))
        joueurs_recherche.insert(0, "prenom_score",
                                 joueurs_df.apply(lambda x: utils.similar(f'{x["prenom"]}', recherche), axis=1))
        joueurs_recherche = joueurs_recherche[
            (joueurs_recherche['prenom_score'] > seuil) | (joueurs_recherche['nom_score'] > seuil)]
        joueurs_recherche.insert(0, "score",
                                 joueurs_recherche.apply(lambda row: max(row["prenom_score"], row["nom_score"]),
                                                         axis=1))

    # Recherche dans les clubs
    clubs_recherche.insert(0, "score_nom_complet",
                           clubs_recherche.apply(lambda x: utils.similar(f'{x["name"]}', recherche), axis=1))
    clubs_recherche.insert(0, "score_short_name",
                           clubs_recherche.apply(lambda x: utils.similar(f'{x["short_name"]}', recherche), axis=1))
    clubs_recherche.insert(0, "score_villes",
                           clubs_recherche.apply(lambda x: utils.similar(f'{x["ville"]}', recherche), axis=1))
    clubs_recherche = clubs_recherche[
        (clubs_recherche['score_nom_complet'] > seuil) | (clubs_recherche['score_short_name'] > seuil) | (
            clubs_recherche['score_villes'] > seuil)]
    clubs_recherche.insert(0, "score", clubs_recherche.apply(
        lambda row: max(max(row["score_nom_complet"], row["score_short_name"]), row["score_villes"]), axis=1))

    joueurs_recherche.sort_values(by="score", ascending=False, inplace=True)
    clubs_recherche.sort_values(by="score", ascending=False, inplace=True)

    joueurs_recherche.reset_index(drop=True, inplace=True)
    clubs_recherche.reset_index(drop=True, inplace=True)

    # On réduit les df de résultat en gardant les éléments tant qu'il n'y a pas un gros écart de score
    stop = False
    for index, row in joueurs_recherche.iterrows():
        if not stop:
            if index != 0:
                if (joueurs_recherche.iloc[index - 1]["score"] - row["score"] > 0.15 or
                        joueurs_recherche.iloc[0]["score"] - row["score"] > 0.2):
                    joueurs_recherche.drop(index, inplace=True)
                    stop = True
        else:
            joueurs_recherche.drop(index, inplace=True)

    stop = False
    for index, row in clubs_recherche.iterrows():
        if not stop:
            if index != 0:
                if clubs_recherche.iloc[index - 1]["score"] - row["score"] > 0.15 or clubs_recherche.iloc[0]["score"] - \
                        row["score"] > 0.2:
                    clubs_recherche.drop(index, inplace=True)
                    stop = True
        else:
            clubs_recherche.drop(index, inplace=True)

    return joueurs_recherche, clubs_recherche


while True:
    choix_graphiques()
