import pytest
import lxml.html
from parsers.actageparser import ActAgeParser
from parsers.rower import Rower
from collections import namedtuple


def test_get_clubs_in_year():
    clubs = [
        {"url": "/clubes/plantilla.php?id=es&c=2", "name": "Cabo"},
        {"url": "/clubes/plantilla.php?id=es&c=94", "name": "Donostiarra"},
        {"url": "/clubes/plantilla.php?id=es&c=8", "name": "Hondarribia"},
        {"url": "/clubes/plantilla.php?id=es&c=37", "name": "Itsasoko ama"},
        {"url": "/clubes/plantilla.php?id=es&c=38", "name": "Kaiku"},
        {"url": "/clubes/plantilla.php?id=es&c=46", "name": "Ondarroa"},
        {"url": "/clubes/plantilla.php?id=es&c=9", "name": "Orio"},
        {"url": "/clubes/plantilla.php?id=es&c=11", "name": "San Juan"},
        {"url": "/clubes/plantilla.php?id=es&c=18", "name": "San Pedro"},
        {"url": "/clubes/plantilla.php?id=es&c=4", "name": "Tiran"},
        {"url": "/clubes/plantilla.php?id=es&c=13", "name": "Urdaibai"},
        {"url": "/clubes/plantilla.php?id=es&c=68", "name": "Zierbena"},
    ]
    actAgeParser = ActAgeParser()
    year_clubs = actAgeParser.get_clubs_in_year(2018, 'act')
    assert all([c['name'] == y['name'] and c['url'] == y['url'] for c, y in zip(clubs, year_clubs)])

def test_parse_rower_data():
    document = ''
    pathname = './pages/act/2018/donostiarra-[\'AITOR-ARANEGI\'].html'
    with open(pathname, 'r', encoding='utf-8') as f:
        document = lxml.html.fromstring(f.read())

    actAgeParser = ActAgeParser()
    data = actAgeParser.parse_rower_detail_data(document)
    historial = [
        {'2018': 'Donostiarra'},
        {'2017': 'Donostiarra'},
        {'2016': 'Donostiarra'},
        {'2015': 'Donostiarra'},
        {'2014': 'Donostiarra'},
        {'2013': 'Donostiarra'},
        {'2012': 'Donostiarra'},
        {'2011': 'Donostiarra'},
        {'2010': 'Donostiarra'},
        {'2009': 'Donostiarra'},
        {'2008': 'Donostiarra'},
        {'2007': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2006': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2005': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2004': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2003': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2002': 'DONOSTIA ARRAUN LAGUNAK'},
        {'2001': 'DONOSTIA ARRAUN LAGUNAK'},
    ]
    rower = Rower('AITOR ARANEGI UGARTEBURU', 'DONOSTIA', '19-05-1989', None, historial)
    assert data == rower
    assert data.historial == rower.historial
