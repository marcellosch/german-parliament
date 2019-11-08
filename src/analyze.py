from collections import defaultdict
from datetime import date, datetime
from typing import List, Tuple
import pdb

import pandas as pd


class Analyzer:

    def __init__(self, csv_file: str):
        self.df = pd.read_csv(csv_file, dtype={'datetime': 'str'},
                              parse_dates=['datetime'])

        self.df['word_count'] = self.df.text.apply(lambda x: len(x.split()))
        self.df.index = self.df['datetime']

        raise NotImplementedError

    def token_timeseries(self, token: str) -> List[Tuple[date, int]]:
        raise NotImplementedError


if __name__ == "__main__":
    raise NotImplementedError
