from bs4 import BeautifulSoup
import os
import json
from company_name import *
from pymongo import MongoClient
import re
import pandas as pd


try:
    cluster = MongoClient("mongodb+srv://tron-schell:Aurf7046@covidresearch0.d3ctd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", serverSelectionTimeoutMS=5000)
    database = cluster['CovidResearch']
    collection = database['entire_doc_employee']
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


#db.entire_doc_employee('CIK', {$or: [{'Secondary Word':"laid off"}, {'Secondary Word':"layoffs"}, {'Secondary Word':"layoff", {'Secondary Word':"furlough"}, {'Secondary Word':"furloughs"}})


documents = []
#count_not_found = 0
primary_wordlist = ['supply chain']
#secondary_wordlist = ['salary reduction', 'reducing', 'benefits']
secondary_wordlist = ['global', 'international', 'country']


not_found = []
foundcount = 1

found_lst = []

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))


for doc in range(int(len(documents))):
    path = str(documents[doc])


    with open(path, 'r') as f:

        current_cik = os.listdir('sec-edgar-filings')

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

        regex = re.compile(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:-]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?(\w){0,4}')

        # Use finditer to math the regex
        #matches = regex.finditer(document['10-K'])


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

        pos_dat.set_index('item', inplace=True)

        #item_1a_raw = document[pos_dat['start'].loc['item1a']]

        #print(re.finditer('item1a'))
        #print(item_1a_raw)

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

                    found = str(doc_paragraphs[j].get_text())

                    # before_found is the instance before the position the primary word was found in, so in that case -1 the index
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

                    #For every secondary word in the secondary word list, run the code below
                    for s_word in range(len(secondary_wordlist)):  

                        if secondary_wordlist[s_word] in found:
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
                                    "Item": 'Entire Document',
                                    "Primary Word" : primary_wordlist[p_word],
                                    "Secondary Word" : secondary_wordlist[s_word],
                                    "Tag": tags,
                                    "match" : found[0:40]
                                }
                            print(found_dict)
                            print('added to database')
                            '''ids = collection.insert_one(found_dict)
                            print('added', ids)'''

                        elif secondary_wordlist[s_word] in after_found and secondary_wordlist[s_word] in before_found:

                            found_dict = {
                                "CIK" : current_cik[doc],
                                "Company Name" : getCompanyName(documents[doc]),
                                "Item": 'Entire Document',
                                "Primary Word" : primary_wordlist[p_word],
                                "Secondary Word" : secondary_wordlist[s_word],
                                "Tag": tags,
                                "before": before_found[0:40],
                                "match" : found[0:40],
                                "after" : after_found[0:40]
                            } 
                            print('added to database')
                            print(found_dict)
                            '''ids = collection.insert_one(found_dict)
                            print('added', ids)'''

                        # If there is a secondary word in the before paragraph, then run the code underneath
                        elif secondary_wordlist[s_word] in before_found:

                            found_dict = {
                                    "CIK" : current_cik[doc],
                                    "Company Name" : getCompanyName(documents[doc]),
                                    "Item": 'Entire Document',
                                    "Primary Word" : primary_wordlist[p_word],
                                    "Secondary Word" : secondary_wordlist[s_word],
                                    "Tag": tags,
                                    "before": before_found[0:40],
                                    "match" : found[0:40]
                                }
                            print('added to database')
                            print(found_dict)
                            '''ids = collection.insert_one(found_dict)
                            print('added', ids)'''

                        # Else if there is a secondary word in the after found paragraph, then run the code underneath
                        elif secondary_wordlist[s_word] in after_found:

                            found_dict = {"CIK" : current_cik[doc],
                                    "Company Name" : getCompanyName(documents[doc]),
                                    "Item": 'Entire Document',
                                    "Primary Word" : primary_wordlist[p_word],
                                    "Secondary Word" : secondary_wordlist[s_word],
                                    "Tag": tags,
                                    "match" : found[0:40],
                                    "after" : after_found[0:40]}
                            print('added to database')
                            print(found_dict)
                            '''ids = collection.insert_one(found_dict)
                            print('added', ids)'''

                        else:
                            pass
                else:
                    continue

