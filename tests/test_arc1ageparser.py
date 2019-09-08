import pytest
import lxml.html
from parsers.arc1ageparser import Arc1AgeParser
from parsers.rower import Rower
from collections import namedtuple


def test_get_clubs_in_year():
    clubs = [
        {"name": "Arkote", "url":f'/clubes/2018/95/1/Arkote/plantilla' },
        {"name": "Astillero", "url":f'/clubes/2018/32/1/Astillero/plantilla' },
        {"name": "Deustu", "url":f'/clubes/2018/99/1/Deustu/plantilla' },
        {"name": "Getaria", "url":f'/clubes/2018/19/1/Getaria/plantilla' },
        {"name": "Hibaika", "url":f'/clubes/2018/6/1/Hibaika/plantilla' },
        {"name": "Isuntza", "url":f'/clubes/2018/89/1/Isuntza/plantilla' },
        {"name": "Lapurdi", "url":f'/clubes/2018/235/1/Lapurdi/plantilla' },
        {"name": "Pedreña", "url":f'/clubes/2018/40/1/Pedrea/plantilla' },
        {"name": "Portugalete", "url":f'/clubes/2018/102/1/Portugalete/plantilla' },
        {"name": "San Juan", "url":f'/clubes/2018/3/1/San Juan/plantilla' },
        {"name": "Zarautz", "url":f'/clubes/2018/16/1/Zarautz/plantilla' },
        {"name": "Zumaia", "url":f'/clubes/2018/17/1/Zumaia/plantilla' },
    ]
    arcAgeParser = Arc1AgeParser()
    year_clubs = arcAgeParser.get_clubs_in_year(2018, 'arc1')
    print(year_clubs)
    assert all([c['name'] == y['name'] and c['url'] == y['url'] for c, y in zip(clubs, year_clubs)])

def test_parse_rower_data():
    document = ''
    pathname = './pages/arc1/2010/Itsasoko ama-[\'ibon-gaztaazpi-zaldua\'].html'
    with open(pathname, 'r', encoding='utf-8') as f:
        document = lxml.html.fromstring(f.read())

    arcAgeParser = Arc1AgeParser()
    data = arcAgeParser.parse_rower_detail_data(document)
    historial = [
        {'2010': 'Itsasoko ama'},
        {'2009': 'Itsasoko ama'},
        {'2008': 'Orio'},
        {'2007': 'Orio'},
        {'2006': 'Orio'},
        {'2005': 'Orio'},
        {'2004': 'Orio'},
        {'2003': 'Orio'},
        {'2002': 'Orio'},
        {'2001': 'Orio'},
        {'2000': 'Orio'},
        {'1999': 'Orio'},
        {'1998': 'Orio'},
        {'1997': 'Orio'},
        {'1996': 'Orio'},
        {'1995': 'Orio'},
        {'1994': 'Orio'},
        {'1993': 'Orio'},
        {'1992': 'Orio'},
        {'1991': 'Orio'},
        {'1990': 'Orio'},
        {'1989': 'Orio'}
    ]
    rower = Rower('Ibon Gaztañazpi Zaldua', 'Orio', None, 42, historial)
    assert data.name == rower.name
    assert data.birthplace == None
    assert data.age == rower.age
    assert len(data.historial) == len(rower.historial)

