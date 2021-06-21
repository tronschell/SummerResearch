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
for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for i in range(0, 3286):
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
            regex = re.compile(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:-]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?(\w){0,4}')

            # Use finditer to math the regex
            matches = regex.finditer(document['10-K'])

            # Write a for loop to print the matches 
            '''
            for match in matches:
                print(match)
            '''

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
                item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]
                item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]
            except:
                #print('cannot seperate sections')
                pass
            count+=1
            
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            item_1a_paragraphs = item_1a_content.findAll('span')
                

            item_7_content = BeautifulSoup(item_7_raw, 'lxml')
            item_7_paragraphs = item_7_content.findAll('span')

            item_7a_content = BeautifulSoup(item_7a_raw, 'lxml')
            item_7a_paragraphs = item_7a_content.findAll('span')


            for x in range(len(primary_wordlist)):
                for j in range(len(item_1a_paragraphs)):
                    if primary_wordlist[x] in item_1a_paragraphs[j].get_text():
                        try:
                            try:
                                before_found = str(item_1a_paragraphs[j-1].get_text())
                                while len(before_found) <= 2:
                                    foundcount +=1
                                    before_found = str(item_1a_paragraphs[j-foundcount].get_text())

                                after_found = str(item_1a_paragraphs[j+1].get_text())
                                while len(after_found) <= 2:
                                    foundcount +=1
                                    after_found = str(item_1a_paragraphs[j-foundcount].get_text())

                                for s_word in range(len(secondary_wordlist)):
                                    if secondary_wordlist[s_word] in before_found:
                                        print("CIK: ", current_cik[i])
                                        print('PRIMARY WORD: ', primary_wordlist[x])
                                        print('SECONDARY WORD: ', secondary_wordlist[s_word])
                                        print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                        print("\tbefore: ",before_found, '\n\n')

                                        found = str(item_1a_paragraphs[j].get_text())
                                        print("\tmatch: ",found, '\n\n')
                                        
                                        if secondary_wordlist[s_word] in after_found:
                                            print("\tafter: ", after_found, '\n\n')
                                        else:
                                            print("----------------------")
                                        
                                    elif secondary_wordlist[s_word] in after_found:
                                        found = str(item_1a_paragraphs[j].get_text())
                                        print("CIK: ", current_cik[i])
                                        print('PRIMARY WORD: ', primary_wordlist[x])
                                        print('SECONDARY WORD: ', secondary_wordlist[s_word])
                                        print('++++++++++ITEM 1A: Risk Factors++++++++++', '\n\n')
                                        print("\tmatch: ",found, '\n\n')

                                        print("\tafter: ",after_found, '\n\n')

                                        if secondary_wordlist[s_word] in before_found:
                                            print("\tafter: ", before_found, '\n\n')
                                        else:
                                            print("----------------------")
                            except:
                                pass
                        except:
                            pass


                for k in range(len(item_7_paragraphs)):
                    if primary_wordlist[x] in item_7_paragraphs[k].get_text():
                        try:
                            try:
                                before_found = str(item_7_paragraphs[k-1].get_text())
                                while len(before_found) <= 2:
                                    foundcount +=1
                                    before_found = str(item_1a_paragraphs[j-foundcount].get_text())

                                after_found = str(item_7_paragraphs[k+1].get_text())
                                while len(after_found) <= 2:
                                    foundcount +=1
                                    after_found = str(item_1a_paragraphs[j-foundcount].get_text())

                                for s_word in range(len(secondary_wordlist)):
                                    if secondary_wordlist[s_word] in before_found:
                                        print("CIK: ", current_cik[i])
                                        print('PRIMARY WORD: ', primary_wordlist[x])
                                        print('SECONDARY WORD: ', secondary_wordlist[s_word])
                                        print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++', '\n\n')
                                        print("\tbefore: ",before_found, '\n\n')

                                        found = str(item_7_paragraphs[k].get_text())
                                        print("\tmatch: ",found, '\n\n')
                                        
                                        if secondary_wordlist[s_word] in after_found:
                                            print("\tafter: ", after_found, '\n\n')
                                        else:
                                            print("----------------------")
                                        
                                    elif secondary_wordlist[s_word] in after_found:
                                        found = str(item_7_paragraphs[k].get_text())
                                        print("CIK: ", current_cik[i])
                                        print('PRIMARY WORD: ', primary_wordlist[x])
                                        print('SECONDARY WORD: ', secondary_wordlist[s_word])
                                        print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++', '\n\n')
                                        print("\tmatch: ",found, '\n\n')

                                        print("\tafter: ",after_found, '\n\n')

                                        if secondary_wordlist[s_word] in before_found:
                                            print("\tafter: ", before_found, '\n\n')
                                        else:
                                            print("----------------------")
                            except:
                                pass
                        except:
                            pass


            item_1a_paragraphs.clear()
            item_7_paragraphs.clear()

        except:
            not_found.append(current_cik[i])
            #print(current_cik[i])
            #print("Cannot find any sections, moving on to the next document...")
            count_not_found += 1
            pass

print(count_not_found)
print((len(documents)-len(not_found))/len(documents))
print(not_found)
