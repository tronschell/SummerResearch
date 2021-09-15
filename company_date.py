import os
from bs4 import BeautifulSoup

def getCompanyDate(CIK):
    documents = []

    for root, dirs, files, in os.walk('sec-edgar-filings'):
        for file in files:
            if file.endswith('.html'):
                documents.append(os.path.join(root, file))

    with open(str(CIK), encoding='utf-8') as f:
        raw = f.read()
        soup = BeautifulSoup(raw, 'lxml')
        try:
            CDate = soup.find('ix:nonnumeric',{'name':'dei:DocumentPeriodEndDate'}).getText()
            return CDate
        except:
            CDate = 'NONE'
            return CDate