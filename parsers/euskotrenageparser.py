import requests
import config
import logging
import os
from parsers.actageparser import ActAgeParser


class EuskotrenAgeParser(ActAgeParser):
    url_base = 'http://www.euskolabelliga.com'
    file_path = config.EUSKOTREN_FILES_PATH 

    def get_main_page(self):
        main_page = requests.get(f'{self.url_base}clubes')
        with open('./liga-arc.html', 'w', encoding='utf-8') as f:
            f.write(main_page.text)
        f.close()

    def get_club_data(self, club, url):
        if not os.path.isfile(os.path.join(self.file_path, club, '.html')):
            print(f'Getting data for {club}: {self.url_base}{url}')
            page = requests.get(f'{self.url_base}{url}')
            with open(f'{self.file_path}/{club}.html', 'w', encoding='utf-8') as f:
                f.write(page.text)
            f.close()

    def get_clubs_in_year(self, year, liga):
        clubs = []
        stats = requests.get(f'http://estropadak.eus/api/sailkapenak?league={liga}&year={year}').json()
        izenak = sorted(list(stats[0]['stats'].keys()))
        act_clubs = {}
        with open(config.EUSKOTREN_TEAM_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                l = line.strip().split(' ', maxsplit=1)
                act_clubs[l[1]] = l[0]
        f.close()
        for izena in izenak:
            try:
                id = act_clubs[izena]
                clubs.append({"name": izena, "url": f'/femenina/clubes/plantilla.php?id=es&c={id}' })
                print(izena)
            except Exception as e:
                print(f'No match for: {izena}')
        return clubs

    def isRower(self, content):
        title = content.cssselect('.fizda')
        logging.info(title)
        if title[0].text.strip() == 'Remera':
            return True
        else:
            return False

    def __init__(self):
        pass
