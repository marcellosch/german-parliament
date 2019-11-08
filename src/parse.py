import csv
import glob
import logging
import os
import pdb
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Dict, Iterable, List

import pandas as pd
from tqdm import tqdm


@dataclass
class PlenaryMinutes:
    '''
    Holds the data of a Plenary Minutes
    '''

    title: str
    date: date
    datetime: datetime
    text: str
    period: int
    type: str
    period_number: int

    def asdict(self) -> Dict:
        return {
            'date': self.date,
            'datetime': self.datetime,
            'title': self.title,
            'text': self.text,
            'period': self.period,
            'type': self.type,
            'period_number': self.period_number
        }

    def tokens(self) -> List[str]:
        raise NotImplementedError


class PlenaryMinutesParser:
    ''' 
    Parses the XML files, processes the data and saves them in csv format. 
    '''

    def parse(self, file_path: str) -> PlenaryMinutes:
        ''' 
        Parse a single file. 
        '''
        xml_elem = ET.parse(file_path).getroot()
        if xml_elem.tag == 'DOKUMENT':
            pm = self.parse_old_format(xml_elem)
        elif xml_elem.tag == 'dbtplenarprotokoll':
            pm = self.parse_new_format(xml_elem)
        else:
            raise RuntimeError(f'Could not parse input file {file_path}')

        return pm

    def parse_all(self, files: Iterable[str]) -> List[PlenaryMinutes]:
        '''
        Parse a list of files.
        '''
        return [self.parse(file) for file in tqdm(files, desc="Parsing xml files.")]

    def parse_old_format(self, xml_file: ET.Element) -> PlenaryMinutes:
        ''' 
        Parser for periods 1 to 18.
        '''
        date = self.parse_date(xml_file.find('DATUM').text)
        dt = datetime.combine(date, time.min)
        title = xml_file.find('TITEL').text
        text = self.clean_text(xml_file.find('TEXT').text)
        period = int(xml_file.find('WAHLPERIODE').text)
        type = xml_file.find('DOKUMENTART').text
        period_number = int(xml_file.find('NR').text.split('/')[-1])

        return PlenaryMinutes(
            date=date,
            datetime=dt,
            title=title,
            text=text,
            period=period,
            type=type,
            period_number=period_number
        )

    def parse_new_format(self, xml_file: ET.Element) -> PlenaryMinutes:
        '''
        Parser for period 19.
        '''
        try:
            date = self.parse_date(xml_file.get('sitzung-datum'))
        except:
            pdb.set_trace()
        dt = datetime.combine(date, time.min)
        title = ''.join([t for t in xml_file.find(
            'vorspann/kopfdaten/sitzungstitel').itertext()])
        text = self.clean_text(
            ''.join([t for t in xml_file.find('sitzungsverlauf').itertext()])
        )
        period = int(xml_file.get('wahlperiode'))
        type = xml_file.tag
        period_number = int(xml_file.get('sitzung-nr'))

        return PlenaryMinutes(
            date=date,
            datetime=dt,
            title=title,
            text=text,
            period=period,
            type=type,
            period_number=period_number
        )

    def parse_date(self, date_str: str) -> date:
        '''
        Parses a date string.
        Format: <day>.<month>.<year>
        Example: 01.12.2019
        '''
        day, month, year = [int(x) for x in date_str.split('.')]
        return date(year=year, month=month, day=day)

    def clean_text(self, text: str) -> str:
        # TODO
        return text.replace('\n', '\\n')

    def save_as_csv(self, pms: List[PlenaryMinutes], path: str = '../data/') -> str:
        ''' Saves the minutes to a csv file. '''
        filepath = os.path.join(path, 'plenary-minutes.csv')
        with open(filepath, 'w') as csvfile:
            fieldnames = [
                'date',
                'datetime',
                'title',
                'period',
                'type',
                'text',
                'period_number'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for pm in tqdm(pms, desc=f'Writing data to {filepath}'):
                writer.writerow(pm.asdict())

        return filepath


def main():
    parser = PlenaryMinutesParser()
    file_iterator = glob.glob('../data/**/*.xml')
    pms = parser.parse_all(file_iterator)
    save_path = parser.save_as_csv(pms)
    logging.info(f'You can find the data at {save_path}')


if __name__ == "__main__":
    main()
