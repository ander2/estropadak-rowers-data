import requests
import lxml.html
import glob
import os
import re


class Arc1AgeParser:
    url_base = 'http://www.liga-arc.com/es/'
    file_path = './pages/arc1'
    staff = [ ]

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
        stats = requests.get(f'http://estropadak.net/api/sailkapena?league={liga}&year={year}').json()
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
                clubs.append({"name": izena, "url":f'/clubes/{year}/{id}/{liga_id}/{_izena}/plantilla' })
            except Exception:
                print(f'No match for: {izena}')
        return clubs

    def get_plantilla_page(self, club, year, url):
        print(f'Getting page for {club}: {self.url_base}{url}')
        page = requests.get(f'{self.url_base}{url}')
        try:
            os.stat(f'{self.file_path}/{year}')
        except FileNotFoundError:
            os.mkdir(f'{self.file_path}/{year}')
        with open(f'{self.file_path}/{year}/{club}.html', 'w', encoding='utf-8') as f:
            f.write(page.text)
        f.close()

    def get_rowers_data(self, club, year):
        with open(f'{self.file_path}/{year}/{club}.html', 'r', encoding='utf-8') as f:
            document = lxml.html.fromstring(f.read())
            links = document.cssselect('.ver-ficha a')
            for link in links:
                link_lst = link.get('href').split('/')
                rower_name = link_lst[-1:]
                print(f'Getting data for {club} {rower_name}')
                page = requests.get(link.get('href'))
                with open(f'{self.file_path}/{year}/{club}-{rower_name}.html', 'w', encoding='utf-8') as f2:
                    f2.write(page.text)
                    continue
        f.close()

    def parse_years_in_rowing(self, content):
        counter = 0
        bad_name = content.cssselect('.nombre-apellidos')[0].text_content()
        full_name = re.sub('([A-Z])', r' \1', bad_name)
        name = full_name.strip()
        for year in content.cssselect('div.historial table tbody tr'):
            cols = year.cssselect('td.club span')
            if len(cols) > 0:
                counter += 1
        return (name, counter)


    def parse_rower_data(self, content):
        name = ''
        name = content.cssselect('.nombre')[0].text.strip()
        age = int(content.cssselect('.edad strong')[0].text.strip())
        print(f'{name} {age}')
        return (name, age)

    def analize_staff_data(self, data):
        ages = []
        average = 0
        for d in data:
            age = d[1]
            ages.append(age)
            average = sum(ages)/len(ages)
        return average


    def analize_rowing_years(self, data):
        years = []
        if len(data) > 0:
            for d in data:
                print(f'{d[0]} {d[1]}')
                years.append(d[1])
            average = sum(years)/len(years)
            return average
        else:
            return None

    def isRower(self, content):
        title = content.cssselect('.fizda')
        if title[0].text.strip() == 'Remero':
            return True
        else:
            return False

    def parse_staff_deep_data(self, club):
        staff_data = []
        for pathname in glob.glob(f'{self.file_path}/{club}-*'):
            with open(pathname, 'r', encoding='utf-8') as f:
                document = lxml.html.fromstring(f.read())
                data = self.parse_years_in_rowing(document)
            staff_data.append(data)
        return self.analize_rowing_years(staff_data)

    def parse_staff_data(self, club, year):
        staff_data = []
        for pathname in glob.glob(f'{self.file_path}/{year}/{club}-*'):
            try:
                print(pathname)
                with open(pathname, 'r', encoding='utf-8') as f:
                    document = lxml.html.fromstring(f.read())
                    data = self.parse_rower_data(document)
                    staff_data.append(data)
            except IndexError:
                pass
        return self.analize_staff_data(staff_data)

    def analize_years(self):
        for club in self.staff:
            average = self.parse_staff_deep_data(club['name'])
            print(f'{club["name"]}: {average}')
            print(10*'-')

    def analize(self, year):
        for club in self.staff:
            average = self.parse_staff_data(club['name'], year)
            print(f'{club["name"]}: {average}')
            print(10*'-')

    def __init__(self):
        pass
