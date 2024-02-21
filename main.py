import pandas as pd
from rich import print
import utils

# Charger les données des fichiers CSV
clubs_df = pd.read_csv("clubs.csv", delimiter=';')
joueurs_df = pd.read_csv("joueurs.csv", delimiter=';')
joueurs_df = pd.merge(joueurs_df, clubs_df, left_on='club', right_on='id', how='left', suffixes=('_joueur', '_club'))


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
        pass  # afficher_classements()
    elif first_choice == "3":
        pass  # afficher_graphiques()
    else:
        print("Choix invalide. Veuillez réessayer.")


def rechercher():
    """Rechercher un joueur ou une équipe"""
    recherche = input("Entrez le nom du joueur ou de l'équipe : ").strip()
    joueurs_recherche, clubs_recherche = compute_recherche(recherche)
    # joueurs_recherche utilisant  utils.similar() pour trouver la liste des éléments les plus probable correspondant
    # à la recherche y compris nom et prénom inversés, seulement un élément ou une équipe

    # Affichage des résultats
    # Si la différence entre le max score des équipes et des joueurs est trop grande, on donne que le plus grand
    # Si il y a 1 seul résultat dans 1 seul df gardé, on prend le résultat
    #  Sinon on affiche une liste et on demande à l'utilisateur de choisir
    if joueurs_recherche.empty and clubs_recherche.empty:
        print("Aucun résultat trouvé")
    elif joueurs_recherche.empty:
        print(clubs_recherche[["name", "short_name", "score"]])
    elif clubs_recherche.empty:
        print(joueurs_recherche[["nom", "prenom", "score"]])
    else:
        if joueurs_recherche.iloc[0]["score"] - clubs_recherche.iloc[0]["score"] > 0.2:
            print(joueurs_recherche[["nom", "prenom", "score"]])
        elif clubs_recherche.iloc[0]["score"] - joueurs_recherche.iloc[0]["score"] > 0.2:
            print(clubs_recherche[["name", "short_name", "score"]])
        else:
            if joueurs_recherche.iloc[0]["score"] > clubs_recherche.iloc[0]["score"]:
                print("Joueurs:")
                print(joueurs_recherche[["nom", "prenom", "score"]])
                print("Clubs:")
                print(clubs_recherche[["name", "short_name", "score"]])
            else:
                print("Clubs:")
                print(clubs_recherche[["name", "short_name", "score"]])
                print("Joueurs:")
                print(joueurs_recherche[["nom", "prenom", "score"]])


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
    rechercher()
