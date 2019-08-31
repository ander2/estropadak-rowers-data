import csv
import sys
import datetime
import pickle
from operator import attrgetter

from parsers.actageparser import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser
from parsers.euskotrenageparser import EuskotrenAgeParser
from parsers.eteageparser import EteAgeParser


def write_to_csv(year, data):
    with open(f'./results/{year}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for taldea in data:
            adin_arabera = sorted(data[taldea], key=lambda arraunlari: datetime.datetime.strptime(arraunlari.birthday, '%d-%m-%Y')) # attrgetter('birthday'))# 
            spamwriter.writerow([taldea])
            for arraunlari in adin_arabera:
                spamwriter.writerow([arraunlari.name, arraunlari.birthday, arraunlari.birthplace])



if __name__ == '__main__':
    liga = sys.argv[1]
    result = {}
    start_year = 2009
    end_year = 2020
    if liga == 'act':
        parser = ActAgeParser()
    elif liga == 'arc1':
        parser = Arc1AgeParser()
        start_year = 2010
    elif liga == 'arc2':
        parser = Arc2AgeParser()
        start_year = 2010
    elif liga == 'euskotren':
        parser = EuskotrenAgeParser()
        start_year = 2011
    elif liga == 'ete':
        parser = EteAgeParser()
        start_year = 2018
    for year in range(start_year, end_year):
        parser.staff = parser.get_clubs_in_year(year, liga)
        data = parser.analize(year)
        result[year] = data
    with open(f'./results/{liga}_data', 'wb') as f:
        pickle.dump(result, f)
