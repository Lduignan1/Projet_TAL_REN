import re

from entity_extraction.per_extraction import PerExtraction
from entity_extraction.loc_extraction import LocExtraction
from entity_extraction.org_extraction import OrgExtraction

def find_titles(text):
    """Match any string that is preceded by an honorific"""
    title_pattern = r'(?:Mr?s?\.?|Dr\.?|M\.|Mmes?|Mlles?|Pr) [A-Z][a-zà-ÿ]+'
    regex_pattern = re.compile(title_pattern)

    res = regex_pattern.findall(text)
    return res


def find_orgs(text):
    """Match any string that is preceded by certain words used in organization names"""
    org_pattern = r'(?:Parti|Association|Fédération|Fondation|Groupe|Institut|Société|Union) [A-zà-ÿ]+ [A-z]*'
    regex_pattern = re.compile(org_pattern)

    res = regex_pattern.findall(text)

    return res

P = PerExtraction()
L = LocExtraction()
O = OrgExtraction()


loc_set = set()


pred_list = []
token_list = []
not_o_tags = []
gold_tags = []

# extracting only the tokens
with open('Corpora/text_test_tokenized_clean.txt', 'r', encoding='utf-8') as file:
    for line in file:
        token_list.append(line.split()[0])
        gold_tags.append(line)

        if ' O' not in line:
            not_o_tags.append(line)
            
# converting corpus to str
corpus = " ".join(token_list)

# adding names recognized by find_title function
per_set = set()
for elt in set(find_titles(corpus)):
    per_set.add(elt.split()[1])

# adding titles recognized by find_title function
title_set = set()
for elt in set(find_titles(corpus)):
    title_set.add(elt.split()[0])

# adding organization titles recognized by find_orgs function
org_set = set()
for elt in set(find_orgs(corpus)):
    org_set.add(elt.split()[0])

# writing NER pred tags onto new file
pred_tags = []
with open('output.txt', 'w+', encoding='utf-8') as file:
    i = 0
    for index, token in enumerate(token_list):
        if token in P.first_names or token in title_set:
            tag = f"{token} B-PER\n"
            file.write(tag)
        elif token in P.last_names or token in per_set:
            tag = f"{token} I-PER\n"
            file.write(tag)
        elif token in O.org or (len(token) > 2 and token.isupper()) or token in org_set:
            tag = f"{token} B-ORG\n"
            file.write(tag)

        elif token in L.loc:
            tag = f"{token} B-LOC\n"
            file.write(tag)
        else:
            tag = f"{token} O\n"
            file.write(tag)

        pred_tags.append(tag)

pred_count = 0
corr_count = 0
for gold,pred in zip(gold_tags, pred_tags):
    if (' O' not in pred):
        pred_count += 1
        if pred == gold and (' O' not in gold):
            corr_count += 1

precision = (corr_count/pred_count)
recall = (corr_count/len(not_o_tags))
fscore = (2 * precision * recall)/(precision + recall)

print(f'Precision: {round(precision, 2)}')
print(f'Recall: {round(recall, 2)}')
print(f'F-score: {round(fscore, 2)}')

if __name__ == '__main__':
    text = "Ms May criticized Mr Johnson while Mrs Obama saluted Dr. Fauci"
    assert find_titles(text) == ['Ms May', 'Mr Johnson', 'Mrs Obama', 'Dr. Fauci']






