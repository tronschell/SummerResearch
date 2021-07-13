from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup

def getCompanyName(CIK):
    documents = []

    for root, dirs, files, in os.walk('sec-edgar-filings'):
        for file in files:
            if file.endswith('.txt'):
                documents.append(os.path.join(root, file))

    with open(str(CIK), 'r', encoding='utf-8') as f:
        raw = f.read()
        soup = BeautifulSoup(raw, 'lxml')
        try:
            CName = soup.find('ix:nonnumeric',{'name':'dei:EntityRegistrantName'}).getText()
            return CName
        except:
            CName = 'NONE'
            return CName

        