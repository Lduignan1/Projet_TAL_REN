from bs4 import BeautifulSoup
import requests

import os


def extract_names_fr():
    """extract French first names from a wikipedia page"""
    html_text = requests.get('https://fr.wikipedia.org/wiki/Liste_de_pr%C3%A9noms_en_fran%C3%A7ais').text
    soup = BeautifulSoup(html_text, 'lxml')

    wikiName = [x.find_all('a') for x in soup.find_all('div', class_='mw-parser-output')]

    list_names = []
    for names in wikiName:
        # add only elements that do not contain whitespaces and start with uppercase followed by lowercase
        list_names.extend([name.text for name in names if
                           ' ' not in name.text and re.search(r"^[A-Z][a-zà-ÿ]+", name.text) is not None])

    list_names.remove(list_names[0])  # delete errant element
    return (set(list_names))


def extract_names_eng():
    """extract English first names from wikipedia pages"""

    # all the wikipedia pages that contain male and female English first names
    urls = [
        'https://en.wikipedia.org/w/index.php?title=Category:English_masculine_given_names&pageuntil=Derek#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:English_masculine_given_names&pageuntil=Jodie#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:English_masculine_given_names&pagefrom=Jodie#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:English_masculine_given_names&pagefrom=Renssalaer#mw-pages',
        'https://en.wikipedia.org/wiki/Category:English_feminine_given_names',
        'https://en.wikipedia.org/w/index.php?title=Category:English_feminine_given_names&pagefrom=Drew+%28name%29#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:English_feminine_given_names&pagefrom=Kirsten+%28given+name%29#mw-pages',
        'https://en.wikipedia.org/w/index.php?title=Category:English_feminine_given_names&pagefrom=Regina+%28name%29#mw-pages']
    list_names = []

    for url in urls:
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        wikiName = [x.find_all('a') for x in soup.find_all('div', class_='mw-category-group')]

        for names in wikiName:
            list_names.extend([name.text for name in names])

        for index, name in enumerate(list_names):
            list_names[index] = re.sub('[\(\[].*?[\)\]]', '', name).rstrip()  # delete text within ()

    return set(list_names)