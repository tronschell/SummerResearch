from bs4 import BeautifulSoup
import os
import json
from company_name import *
from pymongo import MongoClient

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
primary_wordlist = ['COVID-19']
secondary_wordlist = ['layoff', 'layoffs', 'laid off']

not_found = []
foundcount = 1

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
                                    "match" : found
                                }
                            print('added to database')
                            ids = collection.insert_one(found_dict)
                            print('added', ids)

                        elif secondary_wordlist[s_word] in after_found and secondary_wordlist[s_word] in before_found:
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
                                "Item": 'Entire Document',
                                "Primary Word" : primary_wordlist[p_word],
                                "Secondary Word" : secondary_wordlist[s_word],
                                "Tag": tags,
                                "before": before_found,
                                "match" : found,
                                "after" : after_found
                            } 
                            print('added to database')
                            ids = collection.insert_one(found_dict)
                            print('added', ids)

                        # If there is a secondary word in the before paragraph, then run the code underneath
                        elif secondary_wordlist[s_word] in before_found:
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
                                    "before": before_found,
                                    "match" : found
                                }
                            print('added to database')
                            ids = collection.insert_one(found_dict)
                            print('added', ids)

                        # Else if there is a secondary word in the after found paragraph, then run the code underneath
                        elif secondary_wordlist[s_word] in after_found:
                            '''print("CIK: ", current_cik[doc])
                            print('PRIMARY WORD: ', primary_wordlist[p_word])
                            print('SECONDARY WORD:', secondary_wordlist[s_word])
                            print('ENTIRE DOCUMENT', '\n\n')
                            print("\tmatch: ",found, '\n\n')
                            print("\tafter: ",after_found, '\n\n')
                            print("----------------------")'''

                            found_dict = {"CIK" : current_cik[doc],
                                    "Company Name" : getCompanyName(documents[doc]),
                                    "Item": 'Entire Document',
                                    "Primary Word" : primary_wordlist[p_word],
                                    "Secondary Word" : secondary_wordlist[s_word],
                                    "Tag": tags,
                                    "match" : found,
                                    "after" : after_found}
                            print('added to database')
                            ids = collection.insert_one(found_dict)
                            print('added', ids)

                        else:
                            pass
                else:
                    continue

