import requests
from parsers.arc1ageparser import Arc1AgeParser


class Arc2AgeParser(Arc1AgeParser):
    url_base = 'http://www.liga-arc.com/es/'
    file_path = './pages/arc2'

    def __init__(self):
        super()

    def get_clubs_in_year(self, year, liga):
        clubs = []
        talde_id = 2
        stats = requests.get(f'http://estropadak.eus/api/sailkapena?league={liga}&year={year}').json()
        izenak = sorted(list(stats[0]['stats'].keys()))
        liga_clubs = {}
        with open(f'./taldeak_{liga}.txt', 'r', encoding='utf-8') as f:
            for line in f:
                l = line.strip().split(' ', maxsplit=1)
                liga_clubs[l[1]] = l[0]
                print(l[1])
        f.close()
        for izena in izenak:
            try:
                id = liga_clubs[izena]
                _izena = izena.replace('ñ','')
                url = f'/clubes/{year}/{id}/{talde_id}/{_izena}/plantilla'
                r = requests.head(self.url_base + url)
                if r.status_code == 404:
                    talde_id = 1
                    url = f'/clubes/{year}/{id}/{talde_id}/{_izena}/plantilla'
                clubs.append({"name": izena, "url":f'/clubes/{year}/{id}/{talde_id}/{_izena}/plantilla' })
            except Exception:
                print(f'No match for: {izena}')
        return clubs
