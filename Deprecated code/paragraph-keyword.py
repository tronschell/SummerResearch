from bs4 import BeautifulSoup
import re
import os
import time

documents = []

wordlist = ['COVID-19', 'pandemic', 'Coronavirus', 'supply chain']

for root, dirs, files, in os.walk('2020/'):
    for file in files:
        if file.endswith('.html'):
            documents.append(os.path.join(root, file))

for i in range(0, 2):


    current_cik = os.listdir('2020/')
    print("CIK:", current_cik[i])

    path = str(documents[i])
    with open(path, encoding='utf-8') as f:
        document = f.read()
        line_list = f.readlines()

        document_soup = BeautifulSoup(document, 'lxml')

        page = document_soup.findAll('div')

        for a in page:
            paragraphs = document_soup.findAll('p')
            '''
            for b in range(len(paragraphs)):
                paragraph_list.append(paragraphs[b].get_text())
                '''
        
        print(len(page))
        print(len(paragraphs))


        for x in range(len(wordlist)):
            print('WORD:', str(wordlist[x]))
            for y in range(len(paragraphs)):
                if wordlist[x] in paragraphs[y].get_text():
                    try:
                        before_found = str(paragraphs[y-1].get_text())
                        print("before: ",before_found, '\n\n')
                    except:
                        print("before: NONE")
                        pass

                    try:
                        found = str(paragraphs[y].get_text())
                        print("match: ",found, '\n\n')
                    except:
                        print("match: NONE")
                        pass

                    try:
                        after_found = str(paragraphs[y+1].get_text())
                        print("after: ",after_found)
                    except:
                        print("after: NONE")
                        pass
                        
                    print("----------------------")
        paragraphs.clear()
