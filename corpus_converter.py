from bs4 import BeautifulSoup, NavigableString, Tag


# function to flatten a list consisting of strings and lists
def flat2gen(alist):
    for item in alist:
        if isinstance(item, list):
            for subitem in item: yield subitem
        else:
            yield item


def xml_to_txt(xml):
    """
    a (complexe) function that converts an annotated corpus in xml format to
    a list with each element containing a token + its corresponding BIO tag
    :param xml: filename or file object containing XML data
    :return: a list tokenized_text
    """
    tokenized_text = []
    with open(xml, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), "lxml")
        for line in soup.find_all('para'):

            entity_list_para = []
            for element in line:

                # treating blank spaces
                if isinstance(element, NavigableString):
                    element = str(element)

                    entity_list_para.append(element.strip().split())
                    continue

                if element.name == "enamex":
                    value = element.get('type')
                    # print(line)
                    if value == 'Person':
                        tag = 'PER'
                    elif value == 'Organization' or value == 'Company':
                        tag = 'ORG'
                    elif value == 'Location':
                        tag = 'LOC'

                    token_list = element.text.split()
                    for token in token_list:
                        if token == token_list[0]:
                            entity_list_para.append(f'{token} B-{tag}')
                        else:
                            entity_list_para.append(f'{token} I-{tag}')
                else:
                    entity_list_para.append(element.text.split(" "))

            # adding 'O' tag for all non-entities
            for segment in entity_list_para:
                if isinstance(segment, list):
                    for index, token in enumerate(segment):
                        segment[index] = segment[index] + ' ' + 'O'

            tokenized_text.append(list(flat2gen(entity_list_para)))

    return tokenized_text

if __name__ == '__main__':
    # adding each token from corpus to a line in a new file (train)
    with open('text_train_tokenized_clean.txt', 'w+', encoding='utf-8') as file:
        for token in tokenized_text:
            file.write("%s\n" % token)





