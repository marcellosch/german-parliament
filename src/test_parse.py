from parse import PlenaryMinutes, PlenaryMinutesParser
from datetime import date


def test_init():
    parser = PlenaryMinutesParser()
    pm = parser.parse('../data/01-votingperiod/01264.xml')
    assert isinstance(pm.date, date)
    assert len(pm.text) > 0
