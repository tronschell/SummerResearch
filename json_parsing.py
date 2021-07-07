import json
import os

company_names = []
current_cik = os.listdir('2020/')

with open('1_keyword_entire_doc_rich.json') as f:
    data = json.load(f)

    # For every item in the 
    for item in data:
        company_names.append(data[item]['Company Name'])

with open('1_keyword_entire_doc_rich_v2.json') as p:
    data2 = json.load(p)

    for item in data2:
        company_names.append(data2[item]['Company Name'])

print('Total documents: ', len(current_cik))
print('Counted: ', len(set(company_names)))
print(len(set(company_names))/len(current_cik))