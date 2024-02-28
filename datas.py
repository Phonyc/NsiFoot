"""Fichier contenant les données et quelques constantes"""
import pandas as pd

# Charger les données des fichiers CSV
clubs_df = pd.read_csv("clubs.csv", delimiter=';')
joueurs_df = pd.read_csv("joueurs.csv", delimiter=';')

# Ajouter des variables fabriquées
clubs_df["rendement"] = 1 / (clubs_df["rang"] * clubs_df["budget"])
clubs_df["domination"] = ((100 * clubs_df["titres"]) /
                          (2023 - clubs_df["date_crea"]))

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
joueurs_df.insert(0, "age", joueurs_df.apply(
    lambda jx: 2023 - int(jx["birthdate"][:4]), axis=1))

# Création de la variable contenant à la fois le nom et le prénom à des fins de tri par ordre alphabétique
joueurs_df.insert(0, "nom_prenom", joueurs_df.apply(
    lambda jx: f"{jx['nom']} {jx['prenom']}", axis=1))

# Tri par ordre alphabétique + remise à zero de l'index après le tri
joueurs_df.sort_values(by="nom_prenom", inplace=True)
joueurs_df.reset_index(drop=True, inplace=True)
