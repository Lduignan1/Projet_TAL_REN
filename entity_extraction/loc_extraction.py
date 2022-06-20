#LOC
from bs4 import BeautifulSoup
import requests
import re

class LocExtraction:

    def __init__(self):
        self.loc = set()

        self.load_loc_fr()
        self.load_loc_world()
        self.load_cap_world()

    def load_loc_fr(self):
        """extract French locality names from a wikipedia page"""
        urls = [
                'https://fr.wikipedia.org/wiki/Liste_des_d%C3%A9partements_fran%C3%A7ais',
                'https://fr.wikipedia.org/wiki/Liste_des_cantons_fran%C3%A7ais_avant_2015',
                'https://fr.wikipedia.org/wiki/Listes_des_communes_de_France',
                'https://fr.wikipedia.org/wiki/Liste_des_unit%C3%A9s_urbaines_de_France',
                'https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Ville_de_plus_de_100_000_habitants_en_France',
                'https://fr.wikipedia.org/wiki/Cat%C3%A9gorie:Ville_de_50_000_%C3%A0_100_000_habitants_en_France',
                'https://fr.wikipedia.org/wiki/Liste_des_pr%C3%A9fectures_de_France'
        ]
        for url in urls:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')

        wikiLocality = [x.find_all('a') for x in soup.find_all('div', class_='mw-parser-output')]

        list_loc = []
        for locs in wikiLocality:
            # add only elements that do not contain whitespaces and start with uppercase followed by lowercase
            list_loc.extend([loc.text for loc in locs if
                               ' ' not in loc.text and re.search(r"^[A-Z][a-zà-ÿ]+", loc.text) is not None])

        list_loc.remove(list_loc[0])  # delete errant element

        self.loc = self.loc.union((set(list_loc)))

    def load_loc_world(self):
        """extract World locality names from a wikipedia page"""
        urls = [
                'https://fr.wikipedia.org/wiki/Liste_des_%C3%89tats_du_monde_par_continent'
                ]
        for url in urls:
            html_text = requests.get(url).text
            soup = BeautifulSoup(html_text, 'html.parser')

        wikiLocality = [x.find_all('a') for x in soup.find_all('div', class_='mw-parser-output')]

        list_loc = []
        for locs in wikiLocality:
            # add only elements that do not contain whitespaces and start with uppercase followed by lowercase
            list_loc.extend([loc.text for loc in locs if
                               ' ' not in loc.text and re.search(r"^[A-Z][a-zà-ÿ]+", loc.text) is not None])

        list_loc.remove(list_loc[0])  # delete errant element

        self.loc = self.loc.union((set(list_loc)))

    def load_cap_world(self):
        """load all world capitals from a wikipedia page"""

        html_text = requests.get('https://fr.wikipedia.org/wiki/Liste_des_capitales_du_monde').text
        soup = BeautifulSoup(html_text, 'html.parser')

        table = soup.find('table', class_='wikitable sortable alternance')
        for row in table.find_all('tr'):
            cells = row.find_all('td')

        rows = table.find_all('tr')

        lst_data = []

        for row in rows[2:]:
            data = [d.text.rstrip() for d in row.find_all('td')]
            lst_data.append(data[1])

        for index, city in enumerate(lst_data):
            lst_data[index] = re.sub('[\(\[].*?[\)\]]', '', city).rstrip()

        self.loc = self.loc.union((set(lst_data)))







