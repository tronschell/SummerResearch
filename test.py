from bs4 import BeautifulSoup
import os
import json
from company_name import *
import re

documents = []
#count_not_found = 0
primary_wordlist = ['COVID-19']


not_found = []
foundcount = 0
uni_count = 0
count = 0

found_dict = {}

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('2020'):
    dirs.sort()
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))


for doc in range(len(documents)):
    path = str(documents[doc])

    current_cik = os.listdir('2020/')

    with open(path, encoding='utf-8') as f:

        raw_10k = f.read()

        soup = BeautifulSoup(raw_10k, 'lxml')
        print('Checking document number', doc, 'out of', len(documents))

        found_paragraphs = soup.findAll(text=re.compile('COVID-19'))
        print(found_paragraphs)

        if found_paragraphs != []:
            foundcount += 1
            count += 1
            found_paragraphs.clear()
            print('found number:', foundcount)
        else:
            pass

        # Only find 1 paragraph per entire document, if one is found then move onto the next document entirely.
        if count == 1:
            continue
        else:
            pass

        count=0
print(foundcount)
        
