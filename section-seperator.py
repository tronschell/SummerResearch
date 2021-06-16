from bs4 import BeautifulSoup
import re
import pandas as pd
import os

documents = []
count_not_found = 0
wordlist = ['COVID-19', 'pandemic', 'coronavirus', 'supply chain', ]
regex = ""

count = 0
for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.txt'):
            documents.append(os.path.join(root, file))

for i in range(0, 999):
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

        try:
            regex = re.compile(r'(>Item(\s|&#160;|&nbsp;)(1A|1B|7A|7|8)\.{0,1})|(ITEM\s(1A|1B|7A|7|8))|(item\s(1A|1B|2|7A|7|8))')

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


            item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]
            item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]
            item_7a_raw = document['10-K'][pos_dat['start'].loc['item7a']:pos_dat['start'].loc['item8']]
            
            count+=1
            
            item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
            item_1a_paragraphs = item_1a_content.findAll('span')
            '''
            if len(item_1a_paragraphs) < 300:
                item_1a_paragraphs.clear()
                item_1a_paragraphs = item_1a_content.findAll('div')

                for d in range(len(item_1a_paragraphs)):
                    item_1a_paragraphs.insert(d, item_1a_paragraphs.findAll('span')[d])
                    del item_1a_paragraphs(d+1)
                    '''

            item_7_content = BeautifulSoup(item_7_raw, 'lxml')
            item_7_paragraphs = item_7_content.findAll('span')

            item_7a_content = BeautifulSoup(item_7a_raw, 'lxml')
            item_7a_paragraphs = item_7a_content.findAll('span')

            for x in range(len(wordlist)):
                print("CIK: ", current_cik[i])
                print('WORD: ', wordlist[x])
                for j in range(len(item_1a_paragraphs)):
                    if wordlist[x] in item_1a_paragraphs[j].get_text():
                        try:
                            print('++++++++++ITEM 1A: Risk Factors++++++++++')
                            before_found = str(item_1a_paragraphs[j-1].get_text())
                            print("\tbefore: ",before_found, '\n\n')
                        except:
                            print('++++++++++ITEM 1A: Risk Factors++++++++++')
                            print("\tbefore: NONE")
                            pass

                        try:
                            found = str(item_1a_paragraphs[j].get_text())
                            print("\tmatch: ",found, '\n\n')
                        except:
                            print("\tmatch: NONE")
                            pass

                        try:
                            after_found = str(item_1a_paragraphs[j+1].get_text())
                            print("\tafter: ",after_found)
                        except:
                            print("\tafter: NONE")
                            pass

                        print("----------------------")

                for k in range(len(item_7_paragraphs)):
                    if wordlist[x] in item_7_paragraphs[k].get_text():
                        try:
                            print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++')
                            before_found = str(item_7_paragraphs[k-1].get_text())
                            print("\tbefore: ",before_found, '\n\n')
                        except:
                            print('++++++++++ITEM 7: Management’s Discussion and Analysis of Financial Condition and Results of Operations++++++++++')
                            print("\tbefore: NONE")
                            pass

                        try:
                            found = str(item_7_paragraphs[k].get_text())
                            print("match: ",found, '\n\n')
                        except:
                            print("\tmatch: NONE")
                            pass

                        try:
                            after_found = str(item_7_paragraphs[k+1].get_text())
                            print("\tafter: ",after_found)
                        except:
                            print("\tafter: NONE")
                            pass

                        print("----------------------")
                        
                for l in range(len(item_7a_paragraphs)):
                    if wordlist[x] in item_7a_paragraphs[l].get_text():
                        try:
                            print('++++++++++ITEM 7A: Quantitative and Qualitative Disclosures about Market Risk++++++++++')
                            before_found = str(item_7a_paragraphs[l-1].get_text())

                            print("\tbefore: ",before_found, '\n')
                        except:
                            print('++++++++++ITEM 7A: Quantitative and Qualitative Disclosures about Market Risk++++++++++')
                            print("\tbefore: NONE")
                            pass

                        try:
                            found = str(item_7a_paragraphs[l].get_text())
                            print("\tmatch: ",found, '\n')
                        except:
                            print("\tmatch: NONE")
                            pass

                        try:
                            after_found = str(item_7a_paragraphs[l+1].get_text())
                            print("\tafter: ",after_found)
                        except:
                            print("\tafter: NONE")
                            pass

                        print("----------------------")
            item_1a_paragraphs.clear()
            item_7_paragraphs.clear()
            item_7a_paragraphs.clear()
        except:
            print("Cannot find any sections, moving on to the next document...")
            count_not_found += 1
            pass
print(count_not_found)
'''
            p = open(str(count), 'w')
            p.write("Current Word" + str(wordlist[x]))
            p.write(found_1a)
            p.write(found_7)
            p.write(found_7a)
            p.write('--------------------------------', '\n')
            '''