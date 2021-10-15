from bs4 import BeautifulSoup
import os
import json
from company_name import *
from company_date import *
from pymongo import MongoClient
import re
import pandas as pd


documents = []
#count_not_found = 0
covid_word = 'COVID-19'
covid_word_count = 0
supplychain_word = 'supply chain'
supplychain_word_count = 0
benefit_word = 'reduction'
benefit_word_count = 0
furlough_word = 'furlough'
furlough_word_count = 0

primaryword = 'supply chain'
secondaryword = ['international', 'global']
internationalsupplychain_count = 0

not_found = []
foundcount = 1

found_lst = []

data = []

comboparagraph = 0

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))

documents.sort()
for doc in range(int(len(documents))):
#for doc in range(20, 40):
    path = str(documents[doc])

    current_cik = os.listdir('sec-edgar-filings')

    with open(path, encoding='utf-8') as f:

        raw_10k = f.read()

        #Try to run this, if something happens, go to the next document but also increment the count for the amount of things not found

        print('Checking document', documents[doc])
        print('Checking number', doc, 'out of', len(documents))
        #Add all of the paragraphs to the item_1a_paragrpahs list
        doc_content = BeautifulSoup(raw_10k, 'lxml')

        #This block of code finds the tag with the most amount of information inside of it and makes it the primary tag for finding things
        #This was made instead of having different tables/collections for different tags
        p_doc_paragraphs = doc_content.findAll('p')
        span_doc_paragraphs = doc_content.findAll('span')
        font_doc_paragraphs = doc_content.findAll('font')

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

        #print('item 1a: ', test_df[test_df['item'].str.contains(r'item1a')])
        
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
        
        # For every line in the range of the length of the "doc_paragraphs" run the code underneath
        for j in range(len(doc_paragraphs)):

            try:
                found = doc_paragraphs[j].get_text()
            except:
                found = ""
                print('not found MATCH paragraph')
                pass

            try:
                before_found = str(doc_paragraphs[j-1].get_text())
                while len(before_found) <= 2:
                    foundcount +=1
                    before_found = str(doc_paragraphs[j-foundcount].get_text())
            except:
                before_found = 'None'

            # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
            try:
                after_found = str(doc_paragraphs[j+1].get_text())
            # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                while len(after_found) <= 2:
                    foundcount +=1
                    after_found = str(doc_paragraphs[j+foundcount].get_text())
            except:
                after_found = 'None'

            # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
            if covid_word in doc_paragraphs[j].get_text():
                covid_word_count += 1
                print('FOUND COVID-19 keyword')

            if supplychain_word in doc_paragraphs[j].get_text():
                supplychain_word_count += 1
                print('FOUND Supply Chain keyword')

            if furlough_word in doc_paragraphs[j].get_text():
                furlough_word_count += 1
                print('FOUND furlough keyword')
            
            if benefit_word in doc_paragraphs[j].get_text():
                benefit_word_count += 1
                print('FOUND benefit cut keyword')
            

            for i in range(len(secondaryword)):
                if primaryword in doc_paragraphs[j].get_text() and secondaryword[i] in doc_paragraphs[j].get_text():
                    internationalsupplychain_count += 1
                    print('FOUND international supply chain keyword')

            for y in range(len(secondaryword)):
                if secondaryword[y] in found:
                    comboparagraph += 1
                elif secondaryword[y] in before_found:
                    comboparagraph += 1
                elif secondaryword[y] in after_found:
                    comboparagraph += 1

            

    data.append([current_cik[doc], getCompanyName(documents[doc]), getCompanyDate(documents[doc]),covid_word_count, supplychain_word_count,furlough_word_count, benefit_word_count, internationalsupplychain_count, comboparagraph])
    covid_word_count = 0
    supplychain_word_count = 0
    furlough_word_count = 0
    benefit_word_count = 0
    internationalsupplychain_count = 0
    comboparagraph = 0
    
    
#print(data)
df = pd.DataFrame(data, columns=['CIK', 'CompanyName', 'FiscalYearEnd','COVID-19', 'SupplyChain', 'Furlough', 'Benefit Cut',  'InternationalSupplyChain', 'ComboParagraph'])
df.head()

df.to_csv('DATA_FINAL4.csv', index=False ,encoding='utf-8')
                                           
print('converted to a csv') 



