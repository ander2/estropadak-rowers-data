import csv
import sys
import datetime
from operator import attrgetter

from parsers.actageparser import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser
# from parsers.euskotrenageparser import EuskotrenAgeParser
from parsers.eteageparser import EteAgeParser


def write_to_csv(year, league, data):
    with open(f'./results/{league}_{year}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for taldea in data:
            if league == 'act' or league == 'euskotren':
                adin_arabera = sorted(data[taldea], key=lambda arraunlari: datetime.datetime.strptime(arraunlari.birthday, '%d-%m-%Y'))
                spamwriter.writerow([taldea])
                for arraunlari in adin_arabera:
                    spamwriter.writerow([arraunlari.name, arraunlari.birthday, arraunlari.birthplace])
            if 'arc' in league or league == 'ete':
                adin_arabera = sorted(data[taldea], key=lambda arraunlari: arraunlari.age or 0)
                spamwriter.writerow([taldea])
                for arraunlari in adin_arabera:
                    spamwriter.writerow([arraunlari.name, arraunlari.age, arraunlari.birthplace])


if __name__ == '__main__':
    year = sys.argv[1]
    liga = sys.argv[2]
    if liga == 'act':
        parser = ActAgeParser()
    elif liga == 'arc1':
        parser = Arc1AgeParser()
    elif liga == 'arc2':
        parser = Arc2AgeParser()
    elif liga == 'ete':
        parser = EteAgeParser()
    parser.staff = parser.get_clubs_in_year(year, liga)
    data = parser.analize(year)
    write_to_csv(year, liga, data)
