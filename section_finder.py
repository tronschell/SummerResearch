import re
import pandas as pd
from bs4 import BeautifulSoup

def section_finder(document, section, tag):
    regex = re.compile(r'((ITEM)|(Item)|(item))\s?(\&nbsp;)?(\d\w?)[.:-]\s?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?(\&nbsp;)?\s?(\w){0,4}')

    # Use finditer to math the regex
    matches = regex.finditer(document['10-K'])

    # Create the dataframe
    test_df = pd.DataFrame([(x.group(), x.start(), x.end()) for x in matches])

    test_df.columns = ['item', 'start', 'end']
    test_df['item'] = test_df.item.str.lower()

    # Replace any unnecessary characters or strings with a space or no space
    test_df.replace('&#160;',' ',regex=True,inplace=True)
    test_df.replace('&nbsp;',' ',regex=True,inplace=True)
    test_df.replace(' ','',regex=True,inplace=True)
    test_df.replace('\.','',regex=True,inplace=True)
    test_df.replace('>','',regex=True,inplace=True)

    # Drop any duplicates and only keep the last one
    pos_dat = test_df.sort_values('start', ascending=True).drop_duplicates(subset=['item'], keep='last')

    # Set item as the dataframe index
    pos_dat.set_index('item', inplace=True)


    # If the user inputs "item 7" then it returns item 7 and same thing for item 1a
    if section.lower() == "item 7":
        item_7_raw = document['10-K'][pos_dat['start'].loc['item7']:pos_dat['start'].loc['item7a']]
        item_7_content = BeautifulSoup(item_7_raw, 'lxml')
        item_7_paragraphs = item_7_content.findAll(str(tag))
        return item_7_paragraphs
        
    elif section.lower() == "item 1a":
        item_1a_raw = document['10-K'][pos_dat['start'].loc['item1a']:pos_dat['start'].loc['item1b']]
        item_1a_content = BeautifulSoup(item_1a_raw, 'lxml')
        item_1a_paragraphs = item_1a_content.findAll(str(tag))
        return item_1a_paragraphs