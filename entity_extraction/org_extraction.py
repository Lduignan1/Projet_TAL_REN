#ORG
from bs4 import BeautifulSoup
import requests
import re

class OrgExtraction:


    def __init__(self):
        self.org = set()
        self.load_orgs()
    
    def load_orgs(self):
        """extract biggest company names from a wikipedia page"""
        html_text = requests.get(
            'https://fr.wikipedia.org/wiki/Classement_mondial_des_entreprises_leader_par_secteur').text
        soup = BeautifulSoup(html_text, 'html.parser')

        tables = soup.find_all('table', class_='wikitable')
        lst_data = []
        for table in tables[:-1]:

            for row in table.find_all('tr'):
                cells = row.find_all('td')

            rows = table.find_all('tr')

            for row in rows[1:]:
                data = [d.text.rstrip() for d in row.find_all('td')]
                lst_data.append(data[1])

            for index, city in enumerate(lst_data):
                lst_data[index] = re.sub('[\(\[].*?[\)\]]', '', city).rstrip()

        self.org = self.org.union(lst_data)

