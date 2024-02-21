import copy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
import tqdm
import time
from unidecode import unidecode
from difflib import SequenceMatcher
import urllib.parse
import datetime
import dotenv

dotenv.load_dotenv()


class ClubScrapper:
    def __init__(self, clubs: dict) -> None:
        self.clubs = clubs

    @staticmethod
    def load_int(strin):
        try:
            return int(strin)
        except:
            return 0

    @staticmethod
    def similar(a, b):
        """ Similarité de 2 textes"""
        return SequenceMatcher(None, unidecode(a.lower()), unidecode(b.lower())).ratio()

    def joined_files_in(self):
        out = {}
        for file in os.listdir("Scrapper/FilesIn"):
            if file.endswith(".csv"):
                dict_in = {}
                with open("Scrapper/FilesIn/" + file, 'r', encoding='utf-8') as rd:
                    lines = rd.read().split('\n')[1:]
                    for line in lines:
                        dict_in[line.split(";")[0]] = int(line.split(";")[1])

                    for content in self.clubs.values():
                        if content["name"] not in out:
                            out[content["name"]] = {}
                        found = False
                        for k, v in dict_in.items():
                            score = self.similar(
                                unidecode(content["name"].lower()), unidecode(k.lower()))
                            if score >= 0.98:
                                out[content["name"]][file] = v
                                found = True
                            elif score > 0.8:
                                # Limite plus basse pour vérification
                                # print(' ', unidecode(
                                #     content["name"].lower()), unidecode(k.lower()))
                                out[content["name"]][file] = v
                                found = True
                        if not found:
                            print(content["name"], "++++++++++++++++++++++")

        return out

    def get_princ_infos(self):
        print("Récupération des infos principales")
        autres = self.joined_files_in()
        for id, content in tqdm.tqdm(self.clubs.items()):
            lien = (f'{os.getenv("LIEN1")}clubs/stats?id={content["lien"].split("=")[-1]}&seasonId=2022-2023'
                    f'&StatsActiveTab=1')
            resp = requests.get(url=lien, headers={
                'User-Agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(resp, 'html.parser')

            stat_card = soup.select('.stats-card--club')[0]
            self.clubs[id]["rang"] = self.load_int(stat_card.select(
                ".stats-card-points--highlight")[0].text[:-1].replace("e", ""))  # rang
            self.clubs[id]["victoires"] = self.load_int(stat_card.select(
                ".stats-card-thirdList span")[0].text)  # Victoires
            self.clubs[id]["nuls"] = self.load_int(stat_card.select(
                ".stats-card-thirdList span")[2].text)  # Nuls
            self.clubs[id]["defaites"] = self.load_int(stat_card.select(
                ".stats-card-thirdList span")[4].text)  # Defaites
            self.clubs[id]["buts_m"] = self.load_int(
                stat_card.select(".StatsCard-goals span")[1].text)  # buts_m
            self.clubs[id]["buts_e"] = self.load_int(
                stat_card.select(".StatsCard-goals span")[3].text)  # buts_e
            self.clubs[id]["date_crea"] = autres[content["name"]
            ]["dates_creas.csv"]  # Creations
            self.clubs[id]["budget"] = autres[content["name"]
            ]["budgets.csv"]  # Budget
            self.clubs[id]["titres"] = autres[content["name"]
            ]["clubs_victoires.csv"]  # Titres
            time.sleep(0.5)

        if self.clubs[2]["rang"] == 18:
            self.clubs[2]["rang"] = 17  # Bug affichage auxerre
        if self.clubs[12]["rang"] == 15:
            self.clubs[12]["rang"] = 16  # Bug affichage nantes

        with open('Scrapper/out_club_middle.json', 'w', encoding='utf-8') as wr:
            json.dump(self.clubs, wr)


class JoueurScrapper:
    def __init__(self, joueurs: dict) -> None:
        self.pbs = []
        self.joueurs = joueurs
        self.joueurs_out = copy.deepcopy(joueurs)
        self.salaires = {}
        with open('Scrapper/salaires.txt', 'r', encoding='utf-8') as rd:
            lines = rd.read().split('\n')[1:]
            for line in lines:
                self.salaires[unidecode(line.split(";")[1])] = round(
                    (int(line.split(";")[-1]) / 12) / 1000000, 6)
        self.gardiens = {}
        with open('Scrapper/gardiens.txt', 'r', encoding='utf-8') as rd:
            lines = rd.read().split('\n')[1:]
            for line in lines:
                self.gardiens[unidecode(line.split(";")[1])] = int(line.split(";")[11])

    def load_int(self, strin):
        try:
            return int(strin)
        except:
            return 0

    def similar(self, a, b):
        """ Similarité de 2 textes"""
        return SequenceMatcher(None, unidecode(a.lower()), unidecode(b.lower())).ratio()

    def joined_files_in(self):
        out = {}
        for file in os.listdir("Scrapper/FilesIn"):
            if file.endswith(".csv"):
                dict_in = {}
                with open("Scrapper/FilesIn/" + file, 'r', encoding='utf-8') as rd:
                    lines = rd.read().split('\n')[1:]
                    for line in lines:
                        dict_in[line.split(";")[0]] = int(line.split(";")[1])

                    for content in self.clubs.values():
                        if content["name"] not in out:
                            out[content["name"]] = {}
                        found = False
                        for k, v in dict_in.items():
                            score = self.similar(
                                unidecode(content["name"].lower()), unidecode(k.lower()))
                            if score >= 0.98:
                                out[content["name"]][file] = v
                                found = True
                            elif score > 0.8:
                                # Limite plus basse pour vérification
                                print(' ', unidecode(
                                    content["name"].lower()), unidecode(k.lower()))
                                out[content["name"]][file] = v
                                found = True
                        if not found:
                            print(content["name"], "++++++++++++++++++++++")

        return out

    def search_infos_player(self, nom, content, lien_footmercato):
        # time.sleep(1)
        out = {}
        for k, v in self.salaires.items():
            score = self.similar(nom, k)
            if score > 0.90:
                out["salaire"] = v
            elif score > 0.85:
                # print(' ', unidecode(nom.lower()), unidecode(k.lower()))
                out["salaire"] = v

        try:
            lien_ligue1fr = f'{os.getenv("LIEN1")}joueur/stats?id={content["lien"]}&seasonId=2022-2023'
            resp_ligue1fr = requests.get(url=lien_ligue1fr, headers={
                'User-Agent': 'Mozilla/5.0'}).text
            soup_ligue1fr = BeautifulSoup(resp_ligue1fr, 'html.parser')
            stats_item = soup_ligue1fr.select(
                '.InfosStats tbody .InfosStats-row')[-1].select(".InfosStats-item")
            out["matchs_j"] = self.load_int(stats_item[0].text)
            out["buts_m"] = self.load_int(stats_item[2].text)
            out["pass_d"] = self.load_int(stats_item[5].text)
        except Exception as e:
            print('Erreur ligue1.fr', e)

        lien_search_fifaindex = f'{os.getenv("LIEN2")}/search/suggest/?query={urllib.parse.quote(nom)}'
        search_res_fifaindex = requests.get(url=lien_search_fifaindex, headers={
            'User-Agent': 'Mozilla/5.0'}).json()
        if len(search_res_fifaindex) > 0:
            lien_joueur_fifaindex = f'{os.getenv("LIEN2")}{search_res_fifaindex[0]["url"]}'
            resp_fifaindex = requests.get(url=lien_joueur_fifaindex, headers={
                'User-Agent': 'Mozilla/5.0'}).text
            soup_joueur_fifaindex = BeautifulSoup(
                resp_fifaindex, 'html.parser')
            joueur_stats = soup_joueur_fifaindex.select(
                ".row .pt-3 .col-sm-6")[1].select(".card-body p")
            out["taille"] = int(joueur_stats[0].select("span")[1].text[:-2])
            out["poids"] = int(joueur_stats[1].select("span")[1].text[:-2])
            out["meilleur pied"] = joueur_stats[2].span.text
            out["date de naissance texte"] = soup_joueur_fifaindex.select(
                ".row .pt-3 .col-sm-6")[1].select(".card-body p")[3].span.text

        if len(out) < 8 and lien_footmercato != "":
            joueur_merc_res = requests.get(url=lien_footmercato, headers={
                'User-Agent': 'Mozilla/5.0'}).text
            soup_joueur_merc = BeautifulSoup(joueur_merc_res, 'html.parser')
            for row in soup_joueur_merc.select(".blockSingle__container .table")[0].select(".table__row"):
                label = row.select(".table__label")[0].text
                value = row.select(".table__value")[0].text.strip()
                if label == "Taille":
                    if not "taille" in out:
                        out["taille"] = int(value[:-2])
                elif label == "Poids":
                    if not "poids" in out:
                        out["poids"] = int(value[:-2])
                elif label == "Meilleur pied":
                    if not "meilleur pied" in out:
                        out["meilleur pied"] = value.replace(
                            "Droit", "Right").replace("Gauche", "Left")
                elif label == "Âge":
                    if not "date de naissance texte" in out:
                        out["date de naissance texte"] = value

            if not "salaire" in out:
                try:
                    joueur_merc_res_salaire = requests.get(url=lien_footmercato + "salaire", headers={
                        'User-Agent': 'Mozilla/5.0'}).text
                    soup_joueur_merc_salaire = BeautifulSoup(
                        joueur_merc_res_salaire, 'html.parser')
                    out["salaire"] = soup_joueur_merc_salaire.select(".blockHorizontal__contents")[0].select(
                        ".blockHorizontal__content")[1].select(".cardSlide__defaultText")[0].text
                except:
                    pass

        if content["poste"] == "Gardien" and out["matchs_j"] != 0:
            found = False
            for k, v in self.gardiens.items():
                score = self.similar(nom, k)
                if score > 0.95:
                    out["buts_e"] = v
                    found = True
                    break

            if not found:
                print(nom)
                out["buts_e"] = None
        else:
            out["buts_e"] = 0

        return out

    def search_foot_mercato(self):
        i = 0
        for nom, content in tqdm.tqdm(self.joueurs.items()):
            i += 1
            if i < 10000:
                try:
                    lien_search = f'{os.getenv("LIEN3")}query/{urllib.parse.quote(nom)}'
                    search_res = requests.get(url=lien_search, headers={
                        'User-Agent': 'Mozilla/5.0'}).text
                    soup_search = BeautifulSoup(search_res, 'html.parser')
                    endrs = soup_search.select('.searchResultList')

                    if len(endrs) == 1:
                        first_result = endrs[0].select(".identity")[0]
                    else:
                        first_result = endrs[-2].select(".identity")[0]

                    lien_temp = first_result.select("a")[0].attrs["href"]
                    name = first_result.select("a")[0].select("span")[
                        1].text.strip()
                    if self.similar(name, nom) > 0.90:
                        lien = lien_temp

                    infos = self.search_infos_player(nom, content, lien)

                    self.joueurs_out[nom]["infos"] = infos
                except Exception as e:
                    print("ERREUR", nom)
                    print(e)
                    self.pbs.append(nom)
        with open('Scrapper/joueurs_temp.json', 'w', encoding='utf-8') as wr:
            json.dump(self.joueurs_out, wr)
        print(self.pbs)
        with open('Scrapper/pbs.json', 'w', encoding='utf-8') as wr:
            json.dump(self.pbs, wr)


class Scrapper:
    def __init__(self) -> None:
        self.clubs = {}
        self.joueurs = {}

    def get_clubs_list(self):
        resp = requests.get(url=f'{os.getenv("LIEN1")}listejoueurs?seasonId=2022-2023&teamId=17&StatsActiveTab=1',
                            headers={'User-Agent': 'Mozilla/5.0'}).text
        soup = BeautifulSoup(resp, 'html.parser')
        ids = []

        for club_item in soup.select(".CustomSelect-item--club"):
            id = club_item.attrs["rel"]
            if id != '':
                ids.append(int(id))
        return ids

    def get_first_lists(self):
        print("Récupération des listes initiales")
        for idclub in tqdm.tqdm(self.get_clubs_list()):

            resp = requests.get(
                url=f'{os.getenv("LIEN1")}listejoueurs?seasonId=2022-2023&teamId={idclub}&StatsActiveTab=1',
                headers={'User-Agent': 'Mozilla/5.0'}).text
            soup = BeautifulSoup(resp, 'html.parser')
            for player_item in soup.select('.PlayerSearch-row'):
                sts = player_item.find_all(
                    "div", {"class": 'PlayerSearch-item'})
                club_toadd = {"id": idclub, "name": sts[2].a.text.strip(
                ), "lien": sts[2].a.attrs["href"]}
                if idclub not in self.clubs:
                    self.clubs[idclub] = club_toadd

                player_infos = {
                    "nom": sts[0].a.text.strip(),
                    "lien": sts[0].a.attrs["href"].split("=")[-1],
                    "club": club_toadd["name"],
                    "club_lien": club_toadd["lien"],
                    "poste": sts[1].text.strip(),
                }
                self.joueurs[sts[0].a.text.strip()] = player_infos
        scr = ClubScrapper(self.clubs)
        scr.get_princ_infos()
        scr = JoueurScrapper(self.joueurs)
        scr.search_foot_mercato()


class Formateur:
    def __init__(self, clubs, joueurs) -> None:
        self.clubs = clubs
        self.joueurs = joueurs
        self.df_clubs = pd.DataFrame.from_dict(self.clubs).T
        self.df_clubs = self.df_clubs.drop(["lien"], axis=1)
        self.df_clubs = self.df_clubs.apply(self.format_row_club, axis=1)
        print(self.df_clubs)
        print(self.df_clubs.dtypes)
        self.df_joueurs = pd.DataFrame.from_dict(self.joueurs).T
        self.df_joueurs = self.df_joueurs.drop(["lien", "club_lien"], axis=1)
        self.df_joueurs = self.df_joueurs.apply(
            self.format_row, axis=1).dropna().reset_index(drop=True)
        print(self.df_joueurs)

    def get_birth(self, input):
        if "/" in input:
            return datetime.datetime.strptime(input.split("(")[1].split(")")[0], '%d/%m/%Y')
        else:
            return datetime.datetime.strptime(
                input.replace("July", "Jul").replace("June", "Jun").replace("April", "Apr").replace("Sept",
                                                                                                    "Sep").replace(
                    "March", "Mar").replace(".", ""), '%b %d, %Y')

    def get_salaire(self, input):
        if isinstance(input, float):
            return input
        elif isinstance(input, str):
            if "K" in input:
                return int(input.split("K")[0]) / 1000
            else:
                return int(input.split(".")[0]) / 1000000
        else:
            print(input, "??????????????????")

    def format_row_club(self, row):
        row["id"] = int(row["id"])
        row["rang"] = int(row["rang"])
        row["victoires"] = int(row["victoires"])
        row["nuls"] = int(row["nuls"])
        row["defaites"] = int(row["defaites"])
        row["buts_m"] = int(row["buts_m"])
        row["buts_e"] = int(row["buts_e"])
        row["date_crea"] = int(row["date_crea"])
        row["budget"] = int(row["budget"])
        row["titres"] = int(row["titres"])

        return row

    def format_row(self, row):
        nom_dec = unidecode(row["nom"])
        noms = nom_dec.split(' ')
        for idx, mot in enumerate(noms):
            first_index = 0
            if mot.isupper():
                for i in range(idx):
                    first_index += len(noms[i]) + 1
                prenom = row["nom"][:first_index - 1].strip()
                nom_new = row["nom"][first_index:].strip()
                if prenom == "":
                    prenom = nom_new
                row["nom"] = nom_new
                row["prenom"] = prenom
                break

        liste_cars = ["salaire", "matchs_j", "buts_m", "pass_d", "taille", "poids", "meilleur pied",
                      "date de naissance texte", "buts_e"]
        for car in liste_cars:
            row[car] = None

        if str(row["infos"]) != "nan":
            for car in liste_cars:
                if car in row["infos"]:
                    if car not in ["salaire", "date de naissance texte"]:
                        row[car] = row["infos"][car]

                    elif car == "salaire":
                        row["salaire"] = self.get_salaire(row["infos"]["salaire"])
                    elif car == "date de naissance texte":
                        row["birthdate"] = self.get_birth(
                            row["infos"]["date de naissance texte"])

        row["club"] = int(
            self.df_clubs.loc[self.df_clubs['name'] == row["club"]].iloc[0]["id"])
        del row["infos"]
        del row["date de naissance texte"]
        return row

    def save(self, clubs_file, joueurs_file):
        self.df_clubs.to_csv(clubs_file, sep=";", index=False)
        self.df_joueurs.to_csv(joueurs_file, sep=";", index_label="id")


# scr = Scrapper()
# scr.get_first_lists()

frmt = Formateur(clubs=json.load(open('Scrapper/out_club_middle.json', 'r', encoding='utf-8')),
                 joueurs=json.load(open('Scrapper/joueurs_temp.json', 'r', encoding='utf-8')))
frmt.save("clubs.csv", "joueurs.csv")
