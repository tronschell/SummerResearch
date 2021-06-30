from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

documents = []
count_not_found = 0
primary_wordlist = ['COVID-19', 'pandemic']
secondary_wordlist = ['']
regex = ""

not_found = []
foundcount = 1
count = 0
for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for i in range(0, 20):
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
#(Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM(\s|&#160;|&nbsp;)(1A|1B|7A|7|8))|(item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8))|(item(\s|&#160;|&nbsp;)(1A|2|7A|7|8))|(ITEM(\s|&#160;|&nbsp;)(1A|2|7A|7|8))|(Item(\s|&#160;|&nbsp;)(1A|2|7A|7|8))|
        try:
            regex = re.compile(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])

            # Write a for loop to print the matches 
            print(current_cik[i])
            for match in matches:
                print(match)
                
            matches = regex.finditer(document['10-K'])
            # Create the dataframe
            test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

            test_df.columns = ['item', 'start', 'end']
            test_df['item'] = test_df.item.str.lower()

            test_df.head()

            test_df.replace('&#160;',' ',regex=True,inplace=True)
            test_df.replace('&nbsp;',' ',regex=True,inplace=True)
            test_df.replace(' ','',regex=True,inplace=True)
            test_df.replace('\.','',regex=True,inplace=True)
            test_df.replace('>','',regex=True,inplace=True)

            test_df.head()

            pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

            # Display the dataframe
            pos_dat

            # Set item as the dataframe index
            pos_dat.set_index('item', inplace=True)

            # display the dataframe
            pos_dat

            time.sleep(8)

        except:
            pass
