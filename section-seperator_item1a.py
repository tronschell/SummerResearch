from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import time

documents = []
count_not_found = 0
primary_wordlist = ['COVID-19', 'pandemic']
secondary_wordlist = ['supply chain']
regex = ""

not_found = []
foundcount = 1
count = 0

# This finds all of the files with the .txt extension and adds the name of the file to the list called "documents"
for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for doc in range(0, 3286):
    path = str(documents[doc])

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

        #Try to run this, if something happens, go to the next document but also increment the count for the amount of things not found
        try:
            regex = re.compile(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:-]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?(\w){0,4}')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])


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
            try:
                item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]
            except:
                #print('cannot seperate sections')
                item_1a_raw.clear()
                continue
            count+=1
            
            #Add all of the paragraphs to the item_1a_paragrpahs list
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            item_1a_paragraphs = item_1a_content.findAll('span')
            #For every word in the range of the length of the list of "primary_word list" run the code underneath
            for p_word in range(len(primary_wordlist)):

                # For every line in the range of the length of the "item_1a_paragraphs" run the codfe underneath
                for j in range(len(item_1a_paragraphs)):

                    # If an instance of a primary word is somewhere in the "item_1a_paragrpahs list", then run the code underneath
                    if primary_wordlist[p_word] in item_1a_paragraphs[j].get_text():
                        try:
                            found = str(item_1a_paragraphs[j].get_text())

                            # before_found is the instance before the position the primary word was found in, so in that case -1 the index
                            before_found = str(item_1a_paragraphs[j-1].get_text())
                            while len(before_found) <= 2:
                                foundcount +=1
                                before_found = str(item_1a_paragraphs[j-foundcount].get_text())

                            # after_found is the instance after the position the primary word was found in, so in that case  +1 the index
                            after_found = str(item_1a_paragraphs[j+1].get_text())

                            # If the length of the after found paragrpah is less than or equal to 2 characters it is most likely a space, number, or bullet point. In that case, skip it by incrementint
                            while len(after_found) <= 2:
                                foundcount +=1
                                after_found = str(item_1a_paragraphs[j+foundcount].get_text())
                            
                            #For every secondary word in the secondary word list, run the code below
                            for s_word in range(len(secondary_wordlist)):
                                # If there is a secondary word in the before paragraph, then run the code underneath
                                if secondary_wordlist[s_word] in before_found:
                                    print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', primary_wordlist[p_word])
                                    print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                    print("\tbefore: ",before_found, '\n\n')
                                    
                                    print("\tmatch: ",found, '\n\n')
                                    print("----------------------")
                                    # If there is a secondary word in the after found paragraph, then run the code underneath
                                    if secondary_wordlist[s_word] in after_found:
                                        print("\tafter: ", after_found, '\n\n')
                                        print("----------------------")
                                    else:
                                        pass
                                # Else if there is a secondary word in the after found paragraph, then run the code underneath
                                elif secondary_wordlist[s_word] in after_found:
                                    print("CIK: ", current_cik[doc])
                                    print('PRIMARY WORD: ', primary_wordlist[p_word])
                                    print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                    print("\tmatch: ",found, '\n\n')
                                    print("\tafter: ",after_found, '\n\n')
                                    print("----------------------")
                                else:
                                    pass      
                        except:
                            pass
        except:
            not_found.append(current_cik[doc])
            #print(current_cik[doc])
            #print("Cannot find any sections, moving on to the next document...")
            count_not_found += 1
            continue
    # Clear the paragraphs list so that we dont keep appending new data to it without removing the last documents paragraphs
    item_1a_paragraphs.clear()
"""
print(count_not_found)
print((len(documents)-len(not_found))/len(documents))
print(not_found)"""
