import pytest
from parsers.actageparser import ActAgeParser


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
    year_clubs = actAgeParser.get_clubs_in_year(2018)
    assert all([c['name'] == y['name'] and c['url'] == y['url'] for c, y in zip(clubs, year_clubs)])
