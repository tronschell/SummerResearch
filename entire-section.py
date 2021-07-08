from bs4 import BeautifulSoup
import os
import json
from company_name import *
from pymongo import MongoClient

try:
    client = MongoClient('localhost', 27017)
    database = client['CovidResearch']
    collection = database['entire_doc_p']
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")


documents = []
#count_not_found = 0
primary_wordlist = ['COVID-19']
secondary_wordlist = ['supply chain']

not_found = []
foundcount = 1
uni_count = 0

found_lst = []

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))


for doc in range(int(len(documents)/200)):
    path = str(documents[doc])

    current_cik = os.listdir('sec-edgar-filings')

    with open(path, encoding='utf-8') as f:

        raw_10k = f.read()

        #Try to run this, if something happens, go to the next document but also increment the count for the amount of things not found

        print('Checking document', documents[doc])
        print('Checking number', doc, 'out of', len(documents))
        #Add all of the paragraphs to the item_1a_paragrpahs list
        doc_content = BeautifulSoup(raw_10k, 'lxml')
        doc_paragraphs = doc_content.findAll('p')
        #For every word in the range of the length of the list of "primary_word list" run the code underneath
        for p_word in range(len(primary_wordlist)):

            # For every line in the range of the length of the "doc_paragraphs" run the code underneath
            for j in range(len(doc_paragraphs)):

                # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                if primary_wordlist[p_word] in doc_paragraphs[j].get_text():

                    found = str(doc_paragraphs[j].get_text())

                    # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                    before_found = str(doc_paragraphs[j-1].get_text())
                    while len(before_found) <= 2:
                        foundcount +=1
                        before_found = str(doc_paragraphs[j-foundcount].get_text())

                    # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
                    after_found = str(doc_paragraphs[j+1].get_text())

                    # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                    while len(after_found) <= 2:
                        foundcount +=1
                        after_found = str(doc_paragraphs[j+foundcount].get_text())
                    uni_count +=1

                    #For every secondary word in the secondary word list, run the code below
                    for s_word in range(len(secondary_wordlist)):  

                        if secondary_wordlist[s_word] in after_found and secondary_wordlist[s_word] in before_found:
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
                                "before": before_found,
                                "match" : found,
                                "after" : after_found
                            } 
                            print('appended to list')
                            found_lst.append(found_dict.copy())

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
                                    "before": before_found,
                                    "match" : found,
                                    "after" : 'NONE'
                                }
                            print('appended to list')
                            found_lst.append(found_dict.copy())



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
                                    "before": 'NONE',
                                    "match" : found,
                                    "after" : after_found}
                            print('appended to list')
                            found_lst.append(found_dict.copy())

                        else:
                            pass
                else:
                    continue

print(found_lst)


print((len(documents)-len(not_found))/len(documents))
print(not_found)
