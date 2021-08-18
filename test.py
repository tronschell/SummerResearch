from bs4 import BeautifulSoup
import os
import json
from company_name import *
from pymongo import MongoClient
import re
import pandas as pd

try:
    client = MongoClient('localhost', 27017)
    database = client['CovidResearch']
    collection = database['entire_doc_employee']
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


documents = []
#count_not_found = 0
primary_wordlist = ['COVID-19']
secondary_wordlist = ['employee', 'furlough', 'furloughed']

not_found = 0

foundcount = 1

first_count = 0

found_lst = []

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))


for doc in range(int(len(documents))):
    path = str(documents[doc])

    current_cik = os.listdir('sec-edgar-filings')

    with open(path, encoding='utf-8') as f:

        raw_10k = f.read()

        #Try to run this, if something happens, go to the next document but also increment the count for the amount of things not found

        matches = re.finditer(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:-]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?(\w){0,4}', raw_10k)

        test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

        test_df.columns = ['item', 'start', 'end']
        test_df['item'] = test_df.item.str.lower()

        # Replace any unnecessary characters or strings with a space or no space
        test_df.replace('&#160;',' ',regex=True,inplace=True)
        test_df.replace('&nbsp;',' ',regex=True,inplace=True)
        test_df.replace(' ','',regex=True,inplace=True)
        test_df.replace('\.','',regex=True,inplace=True)
        test_df.replace('>','',regex=True,inplace=True)

        print(test_df)

        doc_data = []
        doc_data.extend(test_df['end'].tolist())

        print('Checking document', documents[doc])
        print('Checking number', doc, 'out of', len(documents))
    
        #Add all of the paragraphs to the item_1a_paragrpahs list
        doc_content = BeautifulSoup(raw_10k, 'lxml')

        #This block of code finds the tag with the most amount of information inside of it and makes it the primary tag for finding things
        #This was made instead of having different tables/collections for different tags
        p_doc_paragraphs = doc_content.findAll('p')
        span_doc_paragraphs = doc_content.findAll('span')
        font_doc_paragraphs = doc_content.findAll('font')

        if (len(p_doc_paragraphs) > len(span_doc_paragraphs)) and (len(p_doc_paragraphs) > len(font_doc_paragraphs)):
            print('using p doc paragraphs')
            doc_paragraphs = p_doc_paragraphs
            tags = 'p'
        elif (len(span_doc_paragraphs) > len(p_doc_paragraphs)) and (len(span_doc_paragraphs) > len(font_doc_paragraphs)):
            print('using span paragraphs')
            doc_paragraphs = span_doc_paragraphs
            tags = 'span'
        else:
            doc_paragraphs = font_doc_paragraphs
            tags = 'font'

        #For every word in the range of the length of the list of "primary_word list" run the code underneath
        for p_word in range(len(primary_wordlist)):

            # For every line in the range of the length of the "doc_paragraphs" run the code underneath
            for j in range(len(doc_paragraphs)):

                # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                if primary_wordlist[p_word] in doc_paragraphs[j].get_text():
                    try:

                        print(doc_paragraphs[j].get_text())
                        #Finding the index in the raw text
                        regex_found = re.finditer(str(doc_paragraphs[j].get_text()), raw_10k)
                        #adds the position to a pandas dataframe so we can call it later
                        p_data = pd.DataFrame([(p.group(), p.start(), p.end()) for p in regex_found])
                        print(p_data)
                        #adding column names
                        p_data.columns = ['item', 'start', 'end']
                        
                        #grab the start location of the paragraph from the dataframe
                        p_data_loc = p_data['start'].item()

                        #calculate which number in the doc_data list is the closest to the p_data_loc number
                        closest = min(doc_data, key=lambda x:abs(x-p_data_loc))

                        #set this index variable to the index of the closest number
                        index = doc_data.index(closest)

                        print('item', test_df['item'][index])
         
                        print('----------------------')
                    except:
                        print('skipping')
                        not_found += 1
                        section = 'None'
                        continue
                    print('number not found:', not_found)
                    

                else:
                    continue
                
