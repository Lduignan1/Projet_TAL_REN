import re

from collections import Counter
import xml.etree.ElementTree as ET

from entity_extraction.per_extraction import PerExtraction

per_set = set()
org_set = set()
loc_set = set()

# putting all tokens in test corpus into list
# and attempt to gather ONLY NEs; no tags

with open('text_train_tokenized_clean.txt', 'r', encoding='utf-8') as file:
    for line in file:
        #pred_list.append(line.rstrip())
        if '-PER' in line:
            per_set.add(line.rstrip())
        elif '-ORG' in line:
            org_set.add(line.rstrip())
        elif '-LOC' in line:
            loc_set.add(line.rstrip())

pred_list = []

# extracting only the tokens
with open('text_test_tokenized_clean.txt', 'r', encoding='utf-8') as file:
    for line in file:
        pred_list.append(line.split()[0])

# writing NER pred tags onto new file 
with open('output.txt', 'w+', encoding='utf-8') as file:
    for index, token in enumerate(pred_list):
        duplicate = False

        if token in per_set or token in P.first_names:
            file.write(f"{token} B-PER\n")
        elif token in org_set:
            file.write(f"{token} B-ORG\n")
        elif token in loc_set:
            file.write(f"{token} B-LOC\n")
        else:
            if duplicate:
                continue
            else:
                file.write(f"{token} O\n")

def find_titles(text):
    """Match any string that is preceded by an honorific"""
    title_pattern = r'(?:Mr?s?\.?|Dr\.?|M\.|Mmes?|Mlles?|Pr) [A-Z][a-z]+'
    regex_pattern = re.compile(title_pattern)

    res = regex_pattern.findall(text)
    return res


def find_titles2(text):
    """Match any string that is preceded by an honorific and gives it position"""
    title_pattern = r'(?:Mr?s?\.?|Dr\.?|M\.|Mmes?|Mlles?) [A-z]+'
    regex_pattern = re.compile(title_pattern)

    for m in regex_pattern.finditer(text):
        print('%02d-%02d: %s' % (m.start(), m.end(), m.group(0)))


def count_total_entities(tree):
    count = 0

    # count number of entity tags
    for element in tree.iter('ENAMEX'):
        # print(element.attrib)
        count += 1
    print(f'Number of named entities in whole corpus: {count}')


def count_by_type(root):
    count_per = 0
    count_org = 0
    count_loc = 0

    for enamex_tag in root.findall('news_item/news_text/para/ENAMEX'):
        value = enamex_tag.get('type')
        if value == 'Person':
            # print(enamex_tag.attrib)
            count_per += 1
        elif value == 'Organization' or value == 'Company':
            # print(enamex_tag.attrib)
            count_org += 1
        elif value == 'Location':
            # print(enamex_tag.attrib)
            count_loc += 1

    print(f'Number of PER: {count_per}')
    print(f'Number of ORG: {count_org}')
    print(f'Number of LOC: {count_loc}')


def most_freq_per(per_entities, n):
    """Return n most frequent PER entities from corpus"""
    lst_per_entities = []
    for per_entity in per_entities:
        value = per_entity.get('type')
        if value == 'Person':
            lst_per_entities.append(per_entity.text)

    return Counter(lst_per_entities).most_common(n)


def first_and_last_names(text):
    patterns = ["|".join(first_names), r'[A-Z][a-z]+']

    combined_pattern = "|".join(patterns)
    matches = re.findall(combined_pattern, text)

    for index, token in enumerate(matches):
        if (token not in first_names) and (matches[index - 1] in first_names):
            print(matches[index - 1] + " " + token)
        elif matches[index + 1] in first_names:
            print(token)


if __name__ == '__main__':
    text = "Ms May criticized Mr Johnson while Mrs Obama saluted Dr. Fauci"
    assert find_titles(text) == ['Ms May', 'Mr Johnson', 'Mrs Obama', 'Dr. Fauci']

    P = PerExtraction()
    assert len(P.names) == 2287


