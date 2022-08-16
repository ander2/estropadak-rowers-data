import csv
import click
import datetime
import pickle

from parsers.actageparser import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser
from parsers.euskotrenageparser import EuskotrenAgeParser
from parsers.eteageparser import EteAgeParser


def load_data(liga):
    ''' Load serialized data '''
    data = {}
    try: 
        with open(f'./results/{liga.lower()}_data', 'rb') as f:
            data = pickle.load(f)
    except FileNotFoundError:
        print('Pick file not found')
    return data


def save_data(liga: str, data):
    with open(f'./results/{liga}_data', 'wb') as f:
        pickle.dump(data, f)


def write_to_csv(year, data):
    with open(f'./results/{year}.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='\t',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for taldea in data:
            adin_arabera = sorted(
                data[taldea],
                key=lambda arraunlari: datetime.datetime.strptime(
                    arraunlari.birthday,
                    '%d-%m-%Y'
                )
            )
            spamwriter.writerow([taldea])
            for arraunlari in adin_arabera:
                spamwriter.writerow([
                    arraunlari.name,
                    arraunlari.birthday,
                    arraunlari.birthplace
                ])


@click.command()
@click.option('--start-year', type=click.INT, help='Year to start analysis')
@click.option('--end-year', type=click.INT, help='Year to end analysis')
@click.option('--year', type=click.INT, help='Year to analyze')
@click.argument(
    'liga',
    type=click.Choice([
        'act', 'arc1', 'arc2', 'euskotren', 'ete'
    ]))
def analize(start_year, end_year, year, liga):
    team_data = load_data(liga)
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
    if not year:
        for year in range(start_year, end_year):
            parser.staff = parser.get_clubs_in_year(year, liga)
            data = parser.analize(year)
            team_data[year] = data
    else:
        start_year = year
        end_year = year + 1
        for year in range(start_year, end_year):
            parser.staff = parser.get_clubs_in_year(year, liga)
            data = parser.analize(year)
            team_data[year] = data
    save_data(liga, team_data)


if __name__ == '__main__':
    analize()
 