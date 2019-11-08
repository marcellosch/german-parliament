import io
import os
import re
import zipfile
from typing import List
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


class PlenaryMinutesDownloader:

    def __init__(self, path='../data/'):
        self.path = path

    def download(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

        self.download_plenary_minutes_before_period19(
            self.scrape_urls_before_period19(),
            self.path
        )
        self.download_plenary_minutes_period19(
            self.scrape_urls_period19(),
            self.path
        )

    @staticmethod
    def scrape_urls_period19() -> List[str]:
        ''' 
        Scrapes the urls for the files of the 19th electoral term. 
        '''
        url = "https://www.bundestag.de/ajax/filterlist/de/services/opendata/543410-543410/h_b69eefc37c68a841790b7?limit=5&noFilterSet=true&offset="
        offset = 0

        links = []
        while(True):
            page = requests.get(url+str(offset))
            data = page.text
            soup = BeautifulSoup(data, features='html.parser')
            a_tags = soup.find_all('a')

            for a in a_tags:
                link = a.get('href')
                if 'blob' in link and 'data.xml' in link:
                    links.append(urljoin(url, link))

            if len(a_tags) > 0:
                offset += 5
            else:
                break

        return links

    @staticmethod
    def scrape_urls_before_period19() -> List[str]:
        ''' 
        Scrapes the urls for the pleanry minutes files from period 1 to 18. 
        '''
        url = "https://www.bundestag.de/ajax/filterlist/de/services/opendata/488214-488214/h_b69eef8b4c37c68a841790b2fa29a8a7?limit=5&noFilterSet=true&offset="
        offset = 0

        links = []
        while(True):
            page = requests.get(url+str(offset))
            data = page.text
            soup = BeautifulSoup(data, features='html.parser')
            a_tags = soup.find_all('a')

            for a in a_tags:
                link = a.get('href')
                if '-data.zip' in link:
                    links.append(urljoin(url, link))

            if len(a_tags) > 0:
                offset += 5
            else:
                break

        return links

    @staticmethod
    def download_plenary_minutes_before_period19(urls: List[str], data_folder: str):
        ''' 
        Downloads the plenary minutes XML files from periods 1 to 18. 
        '''
        for url in tqdm(urls, desc="Downloading plenary minutes from period 1 to 18."):
            zname = url.split('/')[-1]
            voting_period = re.search(r'\d+', zname)[0]
            path = os.path.join(data_folder, f'{voting_period}-votingperiod')
            if not os.path.exists(path):
                os.mkdir(path)
                r = requests.get(url)
                zfile = zipfile.ZipFile(io.BytesIO(r.content))
                zfile.extractall(path)

    @staticmethod
    def download_plenary_minutes_period19(urls: List[str], data_folder: str):
        ''' 
        Downloads the plenary minutes XML files for period 19. 
        '''
        folder_path = os.path.join(data_folder, '19-votingperiod')
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        for url in tqdm(urls, desc="Downloading plenary minutes from period 19."):
            fname = url.split('/')[-1]
            file_path = os.path.join(folder_path, fname)
            if not os.path.exists(file_path):
                r = requests.get(url)
                with open(file_path, 'w') as f:
                    f.write(r.text)


def main():
    downloader = PlenaryMinutesDownloader()
    downloader.download()


if __name__ == "__main__":
    main()
