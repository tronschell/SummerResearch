from bs4 import BeautifulSoup
import re
import pandas as pd
import os

documents = []
count_not_found = 0
wordlist = ['COVID-19', 'pandemic', 'coronavirus', 'supply chain', ]
regex = ""
item_1a_raw = ""
item_7a_raw = ""
item_7_raw = ""
not_found = []

count = 0
for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for i in range(0, 999):
    path = str(documents[i])

    current_cik = os.listdir('2020/')

    with open(path, 'r') as f:

        raw_10k = f.read()

        doc_start_pattern = re.compile(r'<DOCUMENT>')
        doc_end_pattern = re.compile(r'</DOCUMENT>')

        type_pattern = re.compile(r'<TYPE>[^\n]+')

        doc_start_is = [x.end() for x in doc_start_pattern.finditer(raw_10k)]
        doc_end_is = [x.start() for x in doc_end_pattern.finditer(raw_10k)]

        doc_types = [x[len('<TYPE>'):] for x in type_pattern.findall(raw_10k)]

        document = {}

        # Create a loop to go through each section type and save only the 10-K section in the dictionary
        for doc_type, doc_start, doc_end in zip(doc_types, doc_start_is, doc_end_is):
            if doc_type == '10-K':
                document[doc_type] = raw_10k[doc_start:doc_end]

        try:
            regex = re.compile(r'(Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))|(item\s(1A|1B|7A|7|8))|(item\s(1A|2|7A|7|8))|(ITEM\s(1A|2|7A|7|8))|(Item\s(1A|2|7A|7|8))')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])

   
            for match in matches:
                print(current_cik[i])
                print(match)
                
            print(len(matches))
        except:
            not_found.append(current_cik)
            print(not_found)
            print('NOT FOUND')
            pass
