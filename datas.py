"""Fichier contenant les données et quelques constantes"""
import pandas as pd

# Charger les données des fichiers CSV
clubs_df = pd.read_csv("datas/clubs.csv", delimiter=';')
joueurs_df = pd.read_csv("datas/joueurs.csv", delimiter=';')

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

# Elements pour les graphiques
GRAPH_ELEMENTS = [
    ("Nom du joueur", False, True, "nom_prenom"), ("Poste", False, True, "poste"),
    ("Age", True, True, "age"),
    ("Poids (en kg)", True, True, "poids"),
    ("Taille (en cm)", True, True, "taille"),
    ("Salaire mensuel (en Millions d'euros)", True, True, "salaire"),
    ("Nombre de buts encaissés", True, True, "buts_e_joueur"),
    ("Nombre de buts Marqués", True, True, "buts_m_joueur"),
    ("Nombre de matchs joués", True, True, "matchs_j"),
    ("Meilleur pied", False, True, "meilleur pied"),
    ("Nombre de passes décisives", True, True, "pass_d"),
    ("Club", False, True, "name"), ("Rang (Club)", True, True, "rang"),
    ("Nombre de Victoires (Club)", True, True, "victoires"),
    ("Nombre de Nuls (Club)", True, True, "nuls"),
    ("Nombre de Défaites (Club)", True, True, "defaites"),
    ("Nombre de buts Marqués (Club)", True, True, "buts_m"),
    ("Nombre de buts encaissés (Club)", True, True, "buts_e"),
    ("Date de création du Club", False, True, "date_crea"),
    ("Budget du Club (en Milions d'euros)", True, True, "budget"),
    ("Nombre de titres du Club", True, True, "titres"),
    ("Rendement du Club (en fonction du rang et du budget)", True, True, "rendement"),
    ("Domination du Club en % d'années titrées", True, True, "domination")
]

# Liste des graphiques recommandés
GRAPH_REC = [
    # (Nom, Paramètre en abscisse, Paramètres en ordonnée)
    ("\033[96m1.\033[0m Nombre de buts marqués par club", 11, [16]),
    ("\033[96m2.\033[0m Nombres de buts (Moyennes) en fonction des postes", 1, [6, 7, 8, 10]),
    ("\033[96m3.\033[0m Salaire moyen en fonction des postes", 1, [5]),
    ("\033[96m4.\033[0m Performances en fonction de la taille moyenne des joueurs du club", 4, [16, 17]),
    ("\033[96m5.\033[0m Poids des joueurs en fonction de leur taille", 4, [3]),
    ("\033[96m6.\033[0m Salaire moyen et budget par club", 11, [5, 19]),
    ("\033[96m7.\033[0m \033[1mGraphiques personnalisés\033[0m", [], []),
]
