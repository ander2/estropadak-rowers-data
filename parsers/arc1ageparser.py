import requests
import lxml.html
import glob
import os
import re
from parsers.rower import Rower
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('estropadak')


class Arc1AgeParser:
    url_base = 'http://www.liga-arc.com/es/'
    file_path = './pages/arc1'
    staff = []

    def get_main_page(self):
        main_page = requests.get(f'{self.url_base}clubes')
        with open('./liga-arc.html', 'w', encoding='utf-8') as f:
            f.write(main_page.text)
        f.close()

    def get_clubs_in_year(self, year, liga):
        clubs = []
        liga_id = 1
        if liga == 'arc2':
            liga_id = 2
        stats = requests.get(f'http://estropadak.eus/api/sailkapenak?league={liga}&year={year}').json()
        izenak = sorted(list(stats[0]['stats'].keys()))
        liga_clubs = {}
        with open(f'./taldeak_{liga}.txt', 'r', encoding='utf-8') as f:
            for line in f:
                (club_id, _, izena) = line.strip().partition(' ')
                liga_clubs[izena] = club_id
        f.close()
        for izena in izenak:
            try:
                id = liga_clubs[izena]
                _izena = izena.replace('ñ', '')
                clubs.append({
                    "name": izena,
                    "url": f'/clubes/{year}/{id}/{liga_id}/{_izena}/plantilla'
                })
            except Exception:
                logger.error('Error while getting clubs in year', exc_info=True)
        return clubs

    def fetch_plantilla_page(self, club, year, url):
        logger.info(f'Getting page for {club}: {self.url_base}{url}')
        page = requests.get(f'{self.url_base}{url}')
        page.encoding = 'utf-8'
        try:
            os.stat(f'{self.file_path}/{year}')
        except FileNotFoundError:
            os.mkdir(f'{self.file_path}/{year}')
        with open(f'{self.file_path}/{year}/{club}.html', 'w', encoding='utf-8') as f:
            f.write(page.text)
        f.close()

    def fetch_rower_pages(self, club, year):
        with open(f'{self.file_path}/{year}/{club}.html', 'r', encoding='utf-8') as f:
            document = lxml.html.fromstring(f.read())
            links = document.cssselect('.ver-ficha a')
            for link in links:
                link_lst = link.get('href').split('/')
                rower_name = link_lst[-1:]
                logger.info(f'Getting data for {club} {rower_name}')
                page = requests.get(link.get('href'))
                page.encoding = 'utf-8'
                with open(f'{self.file_path}/{year}/{club}-{rower_name}.html', 'w', encoding='utf-8') as f2:
                    f2.write(page.text)
                    continue
        f.close()

    def parse_years_in_rowing(self, content):
        historial = []
        for year in content.cssselect('div.historial table tbody tr'):
            cols = year.cssselect('td')
            year = cols[0].text_content()
            club = cols[1].text_content()
            licencia = cols[2].text_content()
            if licencia:
                if club:
                    historial.append({year: club})
                else:
                    historial.append({year: licencia})
        return historial

    def parse_rower_detail_data(self, content):
        counter = 0
        bad_name = content.cssselect('.nombre-apellidos')[0].text_content()
        full_name = re.sub('([A-Z])', r' \1', bad_name)
        try:
            jaiolekua = content.cssselect('.poblacion')[0].text_content()
        except IndexError:
            jaiolekua = None
        try:
            age = int(content.cssselect('.edad strong')[0].text.strip())
        except IndexError:
            age = None

        name = full_name.strip()
        for year in content.cssselect('div.historial table tbody tr'):
            cols = year.cssselect('td.club span')
            if len(cols) > 0:
                counter += 1
        historial = self.parse_years_in_rowing(content)
        return Rower(name, jaiolekua, None, age, historial)

    def parse_rower_data(self, content):
        name = ''
        name = content.cssselect('.nombre')[0].text.strip()
        age = int(content.cssselect('.edad strong')[0].text.strip())
        print(f'{name} {age}')
        return (name, age)

    def isRower(self, content):
        title = content.cssselect('.fizda')
        if title[0].text.strip() == 'Remero':
            return True
        else:
            return False

    def parse_staff_data(self, club, year):
        staff_data = []
        for pathname in glob.glob(f'{self.file_path}/{year}/{club}-*'):
            try:
                with open(pathname, 'r', encoding='utf-8') as f:
                    document = lxml.html.fromstring(f.read())
                    data = self.parse_rower_detail_data(document)
                    staff_data.append(data)
            except IndexError:
                pass
        return staff_data

    def analize(self, year):
        result = {}
        for club in self.staff:
            rowers_data = self.parse_staff_data(club['name'], year)
            result[club['name']] = rowers_data
        return result

    def __init__(self):
        pass
