import requests
import lxml.html
import glob
import logging
import os


class EuskotrenAgeParser:
    url_base = 'http://www.euskolabelliga.com/femenina'
    file_path = './pages/euskotren'
    clubs = [
        {"url": "/clubes/plantilla.php?id=es&c=1432575135", "name": "Arraun"},
        {"url": "/clubes/plantilla.php?id=es&c=10", "name": "hondarribia"},
        {"url": "/clubes/plantilla.php?id=es&c=7", "name": "orio"},
        {"url": "/clubes/plantilla.php?id=es&c=9", "name": "sanjuan"},
    ]

    def get_main_page(self):
        main_page = requests.get(f'{self.url_base}clubes')
        with open('./liga-arc.html', 'w', encoding='utf-8') as f:
            f.write(main_page.text)
        f.close()

    def get_club_data(self, club, url):
        if not os.path.isfile(os.path.join(self.file_path, club ,'.html')):
            print(f'Getting data for {club}: {self.url_base}{url}')
            page = requests.get(f'{self.url_base}{url}')
            with open(f'{self.file_path}/{club}.html', 'w', encoding='utf-8') as f:
                f.write(page.text)
            f.close()

    def get_rowers_data(self, club):
        pass

    def parse_rower_data(self, content):
        name = ''
        surname = ''
        birthday = ''
        for ind, data in enumerate(content.cssselect('span.texto_remero span')):
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
            print(f'{d[0]} {d[1]}: {d[2]}')
            date_lst = d[2].split('-')
            year = int(date_lst[0])
            age = 2018 - year
            ages.append(age)
        average = sum(ages)/len(ages)
        return average

    def isRower(self, content):
        title = content.cssselect('.fizda')
        logging.info(title)
        if title[0].text.strip() == 'Remera':
            return True
        else:
            return False

    def parse_staff_data(self, club):
        staff_data = []
        print(club)
        with open(f'{self.file_path}/{club}.html', 'r', encoding='utf-8') as f:
            document = lxml.html.fromstring(f.read())
            rower_data = document.cssselect('ul.remero li')
            for rower in rower_data:
                print(rower)
                if not self.isRower(rower):
                    continue
                data = self.parse_rower_data(rower)
                staff_data.append(data)
        return self.analize_staff_data(staff_data)

    def analize(self):
        for club in self.clubs:
            self.get_club_data(club['name'], club['url'])
            average = self.parse_staff_data(club['name'])
            print(f'{club["name"]}: {average}')
            print(10*'-')

    def __init__(self):
        pass
