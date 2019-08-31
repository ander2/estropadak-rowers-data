import requests
import lxml.html
import sys

from parsers.actageparser import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser
from parsers.euskotrenageparser import EuskotrenAgeParser
from parsers.eteageparser import EteAgeParser

if __name__ == '__main__':
    year = sys.argv[1]
    liga = sys.argv[2]
    if liga == 'act':
        parser = ActAgeParser()
    elif liga == 'arc1':
        parser = Arc1AgeParser()
    elif liga == 'arc2':
        parser = Arc2AgeParser()
    elif liga == 'euskotren':
        parser = EuskotrenAgeParser()
    elif liga == 'ete':
        parser = EteAgeParser()
    parser.staff = parser.get_clubs_in_year(year, liga)
    print(parser.staff)
    for club in parser.staff:
        print(club['name'])
        print(club['url'])
        parser.get_plantilla_page(club['name'], year, club['url'])
        parser.get_rowers_data(club['name'], year)
    parser.analize(year)
