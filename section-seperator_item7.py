from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from company_name import *
from pymongo import MongoClient
from section_finder import *

try:
    client = MongoClient('localhost', 27017)
    database = client['CovidResearch']
    collection = database['item7_doc']
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

documents = []

primary_wordlist = ['COVID-19']
secondary_wordlist = ['supply chain']

found_lst = []

foundcount = 1

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for doc in range(len(documents)):
        path = str(documents[doc])

        current_cik = os.listdir('sec-edgar-filings')

        with open(path, 'r', encoding = 'utf-8') as f:

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
                item_7_paragraphs = section_finder(document, 'item 7', 'p')
            except:
                continue
            
            print('Checking document', documents[doc])
            print('Checking number', doc, 'out of', len(documents))
            #For every word in the range of the length of the list of "primary_word list" run the code underneath
            for p_word in range(len(primary_wordlist)):

                # For every line in the range of the length of the "item_7_paragraphs" run the codfe underneath
                for j in range(len(item_7_paragraphs)):

                    # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                    if primary_wordlist[p_word] in item_7_paragraphs[j].get_text():
                    
                        found = str(item_7_paragraphs[j].get_text())
                        try:
                            # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                            before_found = str(item_7_paragraphs[j-1].get_text())
                            while len(before_found) <= 2:
                                foundcount +=1
                                before_found = str(item_7_paragraphs[j-foundcount].get_text())
                        except:
                            before_found = 'None'
                            
                        try:
                            # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
                            after_found = str(item_7_paragraphs[j+1].get_text())
                            # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                            while len(after_found) <= 2:
                                foundcount +=1
                                after_found = str(item_7_paragraphs[j+foundcount].get_text())
                        except:
                            after_found = 'None'

                        #For every secondary word in the secondary word list, run the code below
                        for s_word in range(len(secondary_wordlist)):
                            if secondary_wordlist[s_word] in after_found and secondary_wordlist[s_word] in before_found:
                                try:
                                    '''print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', primary_wordlist[p_word])
                                    print('SECONDARY WORD:', secondary_wordlist[s_word])
                                    print('ENTIRE DOCUMENT', '\n\n')
                                    print("\tmatch: ",found, '\n\n')
                                    print("\tafter: ",after_found, '\n\n')
                                    print("----------------------")'''

                                    found_dict = {
                                        "CIK" : current_cik[doc],
                                        "Company Name" : getCompanyName(documents[doc]),
                                        "Item": '7: Management’s Discussion and Analysis of Financial Condition and Results of Operations',
                                        "Primary Word" : primary_wordlist[p_word],
                                        "Secondary Word" : secondary_wordlist[s_word],
                                        "Tag": str('span'),
                                        "before": before_found,
                                        "match" : found,
                                        "after" : after_found
                                    } 
                                    print('added to database')
                                    ids = collection.insert_one(found_dict)
                                    print('added', ids)
                                except:
                                    pass

                            # If there is a secondary word in the before paragraph, then run the code underneath
                            elif secondary_wordlist[s_word] in before_found:
                                try:
                                    '''print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', primary_wordlist[p_word])
                                    print('SECONDARY WORD:', secondary_wordlist[s_word])
                                    print('ENTIRE DOCUMENT', '\n\n')

                                    print("\tbefore: ",before_found, '\n\n')
                                    print("\tmatch: ",found, '\n\n')
                                    print("----------------------")'''

                                    found_dict = {
                                            "CIK" : current_cik[doc],
                                            "Company Name" : getCompanyName(documents[doc]),
                                            "Item": '7: Management’s Discussion and Analysis of Financial Condition and Results of Operations',
                                            "Primary Word" : primary_wordlist[p_word],
                                            "Secondary Word" : secondary_wordlist[s_word],
                                            "Tag": str('span'),
                                            "before": before_found,
                                            "match" : found
                                        }
                                    print('added to database')
                                    ids = collection.insert_one(found_dict)
                                    print('added', ids)
                                except:
                                    pass


                            # Else if there is a secondary word in the after found paragraph, then run the code underneath
                            elif secondary_wordlist[s_word] in after_found:
                                try:
                                    '''print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', primary_wordlist[p_word])
                                    print('SECONDARY WORD:', secondary_wordlist[s_word])
                                    print('ENTIRE DOCUMENT', '\n\n')
                                    print("\tmatch: ",found, '\n\n')
                                    print("\tafter: ",after_found, '\n\n')
                                    print("----------------------")'''

                                    found_dict = {"CIK" : current_cik[doc],
                                            "Company Name" : getCompanyName(documents[doc]),
                                            "Item": '7: Management’s Discussion and Analysis of Financial Condition and Results of Operations',
                                            "Primary Word" : primary_wordlist[p_word],
                                            "Secondary Word" : secondary_wordlist[s_word],
                                            "Tag": str('span'),
                                            "match" : found,
                                            "after" : after_found}
                                    print('added to database')
                                    ids = collection.insert_one(found_dict)
                                    print('added', ids)
                                except:
                                    pass
                            else:
                                pass      


