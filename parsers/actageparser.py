import os
import requests
import lxml.html
import glob


class ActAgeParser:
    url_base = 'http://euskolabelliga.com'
    file_path = './pages/act'
    staff = []

    def get_main_page(self, year):
        main_page = requests.get(self.url_base)
        with open(f'./pages/act/{year}/euskolabel.html', 'w', encoding='utf-8') as f:
            f.write(main_page.text)
        f.close()

    def get_clubs_in_year(self, year):
        clubs = []
        stats = requests.get(f'http://estropadak.net/api/sailkapena?league=act&year={year}').json()
        izenak = sorted(list(stats[0]['stats'].keys()))
        act_clubs = {}
        with open(f'./taldeak_act_.txt', 'r', encoding='utf-8') as f:
            for line in f:
                l = line.strip().split(' ', maxsplit=1)
                act_clubs[l[1]] = l[0]
                print(l[1])
        f.close()
        for izena in izenak:
            try:
                id = act_clubs[izena]
                clubs.append({"name": izena, "url":f'/clubes/plantilla.php?id=es&c={id}' })
            except Exception as e:
                print(f'No match for: {izena}')
        return clubs


    def get_plantilla_page(self, club, year, url):
        print(f'Getting page for {club}: {self.url_base}{url}')
        page = requests.get(f'{self.url_base}{url}&t={year}')
        try:
            os.stat(f'./pages/act/{year}')
        except FileNotFoundError:
            os.mkdir(f'./pages/act/{year}')
        with open(f'./pages/act/{year}/{club}.html', 'w', encoding='utf-8') as f:
            f.write(page.text)
        f.close()

    def get_rowers_data(self, club):
        if club == 'cabo':
            return
        with open(f'{self.file_path}/{club}.html', 'r', encoding='utf-8') as f:
            document = lxml.html.fromstring(f.read())
            rowers = document.cssselect('.cuadro_remero')
            for rower in rowers:
                link = rower.cssselect('a.fizda')
                (name, surname, birthday) = self.parse_rower_data(rower)
                print(f'Getting data for {club} {name} {surname}')
                if len(link) == 0:
                    continue
                page = requests.get(self.url_base + link[0].get('href'))
                with open(f'{self.file_path}/{club}-[\'{name}-{surname}\'].html', 'w', encoding='utf-8') as f2:
                    f2.write(page.text)
                continue
        f.close()

    def parse_years_in_rowing(self, content):
        counter = 0
        name = content.cssselect('h3.clasificacion:not(.historial)')[0].text.strip()
        for year in content.cssselect('table.historial tbody tr'):
            cols = year.cssselect('td')
            if cols[1].text is not None:
                counter += 1
        return (name, counter)

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

    def parse_staff_data(self, content):
        staff_data = []
        document = lxml.html.fromstring(content)
        rower_data = document.cssselect('#menudirectiva + ul.remero li')
        for rower in rower_data:
            if not self.isRower(rower):
                continue
            data = self.parse_rower_data(rower)
            staff_data.append(data)
        return self.analize_staff_data(staff_data)

    def analize_years(self):
        ''' Analize rowers experience '''
        for club in self.staff:
            average = self.parse_staff_deep_data(club['name'])
            print(f'{club["name"]}: {average}')
            print(10*'-')

    def analize(self, year):
        ''' Analize rowers' age '''
        for club in self.staff:
            with open(f'./pages/act/{year}/{club["name"]}.html', 'r', encoding='utf-8') as f:
                average = self.parse_staff_data(f.read())
                print(f'{club["name"]}: {average}')
                print(10*'-')
            f.close()

    def __init__(self):
        pass
