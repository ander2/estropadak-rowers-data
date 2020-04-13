'''Fix bad encoding for pages in ARC and ETE leagues'''
import glob
import requests


def fix(club, year):
    file_path = './pages/arc1'
    for pathname in glob.glob(f'{file_path}/{year}/{club}-*'):
        with open(pathname, 'r+', encoding='utf-8') as f:
            document = f.read()
            fixed_doc = document.encode('iso-8859-1').decode('utf-8')
            f.write(fixed_doc)


def get_clubs_in_year(year, liga):
    clubs = []
    liga_id = 1
    stats = requests.get(f'http://estropadak.eus/api/sailkapena?league={liga}&year={year}').json()
    izenak = sorted(list(stats[0]['stats'].keys()))
    return izenak

if __name__ == "__main__":

    liga = 'arc1'
    for year in range(2009, 2020):
        print(f'==== Fixing {year} ==== ')
        klubak = get_clubs_in_year(year, liga)
        for klub in klubak:
            print(f'****  {klub} **** ')
            fix(klub, year)

