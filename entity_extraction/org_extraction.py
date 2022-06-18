#ORG
from bs4 import BeautifulSoup
import requests
import re

class OrgExtraction:

    def __init__(self):
        self.org = set()
        self.load_org_fr()
    
    def load_org_fr(self):
      """extract french organisation names from a wikipedia page"""
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

      wikiOrganisation = [x.find_all('a') for x in soup.find_all('div', class_='mw-parser-output')]

      list_org = []
      for orgs in wikiOrganisation:
            # add only elements that do not contain whitespaces and start with uppercase followed by lowercase
            list_org.extend([org.text for org in orgs if ' ' not in org.text and re.search(r"^[A-Z][a-zà-ÿ]+", org.text) is not None])

      list_org.remove(list_org[0])  # delete errant element

      self.org = self.org.union((set(list_org)))
