from sec_edgar_downloader import Downloader
import os
from bs4 import BeautifulSoup

def getCompanyName(CIK):
    documents = []

    for root, dirs, files, in os.walk('2020/'):
        for file in files:
            if file.endswith('.txt'):
                documents.append(os.path.join(root, file))

    with open(str(CIK), 'r') as f:
        raw = f.read()
        soup = BeautifulSoup(raw, 'lxml')
        CName = soup.find('ix:nonnumeric',{'name':'dei:EntityRegistrantName'})
        return CName.getText()

        