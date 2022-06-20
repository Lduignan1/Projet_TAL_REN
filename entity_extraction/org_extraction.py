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
              'https://fr.wikipedia.org/wiki/Liste_d%27associations_fran%C3%A7aises_reconnues_d%27utilit%C3%A9_publique',
              'https://fr.wikipedia.org/wiki/Organisations_internationales_si%C3%A9geant_en_France',
              'https://fr.wikipedia.org/wiki/Liste_des_organisations_de_solidarit%C3%A9_internationale_fran%C3%A7aises',
              'https://fr.wikipedia.org/wiki/Institutions_de_la_R%C3%A9publique_fran%C3%A7aise',
              'https://fr.wikipedia.org/wiki/Liste_des_partis_politiques_sous_la_Cinqui%C3%A8me_R%C3%A9publique',
              'https://fr.wikipedia.org/wiki/Liste_de_sigles_de_l%27Organisation_des_Nations_unies'
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
