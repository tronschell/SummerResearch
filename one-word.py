from bs4 import BeautifulSoup
import os
import json
from company_name import *
from pymongo import MongoClient

'''try:
    client = MongoClient('localhost', 27017)
    database = client['CovidResearch']
    collection = database['entire_doc_test']
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")'''

documents = []
#count_not_found = 0
primary_wordlist = ['COVID-19']

not_found = []
foundcount = 1
count = 0
zero_found = 0

found_lst = []

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('sec-edgar-filings'):
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))


for doc in range(len(documents)):
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
        try:
            #For every word in the range of the length of the list of "primary_word list" run the code underneath
            for p_word in range(len(primary_wordlist)):
                run_count = 0
                # For every line in the range of the length of the "doc_paragraphs" run the code underneath
                for j in range(len(doc_paragraphs)):

                    # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                    if primary_wordlist[p_word] in doc_paragraphs[j].get_text():
                        if run_count == 1:
                            continue
                        else:
                            pass

                        found = str(doc_paragraphs[j].get_text())
                        run_count += 1
                        print(run_count)
                        #print(found)


                        # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                        try:
                            before_found = str(doc_paragraphs[j-1].get_text())
                            while len(before_found) <= 2:
                                foundcount +=1
                                before_found = str(doc_paragraphs[j-foundcount].get_text())
                        except:
                            before_found='None'

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
                        found_dict = {
                            "CIK" : current_cik[doc],
                            "Company Name" : getCompanyName(documents[doc]),
                            "Item": 'Entire Document',
                            "Primary Word" : primary_wordlist[p_word],
                            "Tag": tags,
                            "before": before_found,
                            "match" : found,
                            "after" : after_found
                        } 
                        print('added to database')
                        '''ids = collection.insert_one(found_dict)
                        print('added', ids)'''
                    else:
                        continue
        except:
            zero_found += 1
            print('cannot find anything, moving on')
            continue

print(zero_found)
