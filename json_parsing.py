import json
import os

company_names = []
current_cik = os.listdir('2020/')

with open('item_7_rich.json') as f:
    data = json.load(f)

    # For every item in the 
    for item in data:
        print('\n')
        
        print(data[item]['Company Name'])
        company_names.append(data[item]['Company Name'])
print('Total documents: ', len(current_cik))
print('Counted: ', len(set(company_names)))
print(len(set(company_names))/len(current_cik))