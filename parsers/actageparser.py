import os
import requests
import lxml.html
import glob
from parsers.rower import Rower


class ActAgeParser:
    url_base = 'http://euskolabelliga.com'
    file_path = './pages/act'
    staff = []

    def get_main_page(self, year):
        main_page = requests.get(self.url_base)
        file_path = f'./pages/act/{year}/euskolabel.html'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(main_page.text)
        f.close()

    def get_clubs_in_year(self, year, liga):
        clubs = []
        url = f'http://estropadak.eus/api/sailkapenak?league={liga}&year={year}'
        stats = requests.get(url).json()
        izenak = sorted(list(stats[0]['stats'].keys()))
        act_clubs = {}
        with open('./taldeak_act_.txt', 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip().split(' ', maxsplit=1)
                act_clubs[line[1]] = line[0]
        f.close()
        for izena in izenak:
            try:
                id = act_clubs[izena]
                clubs.append({
                    "name": izena,
                    "url": f'/clubes/plantilla.php?id=es&c={id}'
                })
                print(izena)
            except Exception as e:
                print(f'No match for: {izena}')
        return clubs

    def fetch_plantilla_page(self, club, year, url):
        print(f'Getting page for {club}: {self.url_base}{url}')
        page = requests.get(f'{self.url_base}{url}&t={year}')
        try:
            os.stat(f'{self.file_path}/{year}')
        except FileNotFoundError:
            os.mkdir(f'{self.file_path}/{year}')
        file_path = f'{self.file_path}/{year}/{club}.html'
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(page.text)
        f.close()

    def fetch_rower_pages(self, club, year):
        if club == 'cabo':
            return
        _club = club.lower().replace(' ', '')
        file_path = f'{self.file_path}/{year}/{club}.html'
        with open(file_path, 'r', encoding='utf-8') as f:
            document = lxml.html.fromstring(f.read())
            rowers = document.cssselect('.cuadro_remero')
            for rower in rowers:
                link = rower.cssselect('a.fizda')
                (name, surname, birthday) = self.parse_rower_data(rower)
                print(f'Getting data for {club} {name} {surname}')
                if len(link) == 0:
                    continue
                rower_page = f'{self.file_path}/{year}/{_club}-[\'{name}-{surname}\'].html'
                try:
                    os.stat(rower_page)
                except FileNotFoundError:
                    page = requests.get(self.url_base + link[0].get('href'))
                    with open(rower_page, 'w', encoding='utf-8') as f2:
                        f2.write(page.text)
        f.close()

    def parse_years_in_rowing(self, content):
        counter = 0
        historial = []
        for year in content.cssselect('table.historial tbody tr'):
            cols = year.cssselect('td')
            if cols[1].text is not None:
                historial.append({cols[0].text: cols[1].text})
                counter += 1
        return historial

    def parse_rower_data(self, content):
        name = ''
        surname = ''
        birthday = ''
        for ind, data in enumerate(content.cssselect('span.texto_remero2 span')):
            if ind == 0:
                name = data.text.strip()
            if ind == 1:
                surname = data.text.strip()
            if ind == 5:
                birthday = data.text.strip()
        return (name, surname, birthday)

    def analize_staff_data(self, data):
        ages = []
        for d in data:
            print(f'{d[0]} {d[1]}')
            date_lst = d[2].split('-')
            year = int(date_lst[2])
            age = 2018 - year
            ages.append(age)
        average = sum(ages)/len(ages)
        return average

    def parse_rower_detail_data(self, content):
        birthday = ''
        jaiolekua = ''
        name = content.cssselect('h3.clasificacion')[0].text.strip()
        for ind, data in enumerate(content.cssselect('.datosRemero span')):
            if ind == 1:
                jaiolekua = data.text.strip()
            if ind == 2:
                birthday = data.text.strip()
        historial = self.parse_years_in_rowing(content)
        return Rower(name, jaiolekua, birthday, None, historial)

    def analize_rowing_years(self, data):
        years = []
        for d in data:
            print(f'{d[0]} {d[1]}')
            years.append(d[1])
        average = sum(years)/len(years)
        return average

    def isRower(self, content):
        title = content.cssselect('.fizda')
        if title[0].text.strip() == 'Remero':
            return True
        else:
            return False

    def parse_staff_deep_data(self, club):
        staff_data = []
        print(club)
        for pathname in glob.glob(f'./{self.file_path}/{club}-*'):
            try:
                with open(pathname, 'r', encoding='utf-8') as f:
                    document = lxml.html.fromstring(f.read())
                    data = self.parse_years_in_rowing(document)
                staff_data.append(data)
            except IndexError:
                pass
        return self.analize_rowing_years(staff_data)

    def parse_staff_data(self, year, club):
        staff_data = []
        _club = club.lower().replace(' ', '')
        for pathname in glob.glob(f'{self.file_path}/{year}/{_club}-*'):
            try:
                print(pathname)
                with open(pathname, 'r', encoding='utf-8') as f:
                    document = lxml.html.fromstring(f.read())
                    data = self.parse_rower_detail_data(document)
                    staff_data.append(data)
            except IndexError:
                pass
        return staff_data

    def analize_years(self):
        ''' Analize rowers experience '''
        for club in self.staff:
            average = self.parse_staff_deep_data(club['name'])
            print(f'{club["name"]}: {average}')
            print(10*'-')

    def analize(self, year):
        ''' Analize rowers' age '''
        result = {}
        for club in self.staff:
            print(club['name'])
            club_name = club['name'].lower()
            rowers_data = self.parse_staff_data(year, club_name)
            result[club['name']] = rowers_data
        return result

    def __init__(self):
        pass
