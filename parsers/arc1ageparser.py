import requests
import lxml.html
import glob

class Arc1AgeParser:
  url_base = 'http://www.liga-arc.com/es/'
  file_path = './pages/arc1'
  clubs = [
    {"url": "/clubes/index.php?id=es&c=2", "name": "cabo"},
    {"url": "/clubes/index.php?id=es&c=4", "name": "tiran"},
    {"url": "/clubes/index.php?id=es&c=8", "name": "hondarribia"},
    {"url": "/clubes/index.php?id=es&c=9", "name": "orio"},
    {"url": "/clubes/index.php?id=es&c=38", "name": "kaiku"},
    {"url": "/clubes/index.php?id=es&c=46", "name": "ondarroa"},
    {"url": "/clubes/index.php?id=es&c=94", "name": "donostiarra"},
    {"url": "/clubes/index.php?id=es&c=11", "name": "sanjuan"},
    {"url": "/clubes/index.php?id=es&c=18", "name": "sanpedro"},
    {"url": "/clubes/index.php?id=es&c=37", "name": "santurtzi"},
    {"url": "/clubes/index.php?id=es&c=13", "name": "urdaibai"},
    {"url": "/clubes/index.php?id=es&c=68", "name": "zierbena"},
  ]

  staff = [
    {'url': 'clubes/2018/95/1/arkote-helvetia/plantilla', 'name': 'ARKOTE-HELVETIA'},
    {'url': 'clubes/2018/32/1/astillero-san-jose-xv/plantilla', 'name': 'ASTILLERO-SAN JOSE XV'},
    {'url': 'clubes/2018/99/1/deusto-bilbao/plantilla', 'name': 'DEUSTO-BILBAO'},
    {'url': 'clubes/2018/19/1/getaria/plantilla', 'name': 'GETARIA'},
    {'url': 'clubes/2018/6/1/hibaika/plantilla', 'name': 'HIBAIKA'},
    {'url': 'clubes/2018/89/1/lekittarra-elecnor-bm/plantilla', 'name': 'LEKITTARRA-ELECNOR-BM'},
    {'url': 'clubes/2018/235/1/lapurdi/plantilla', 'name': 'LAPURDI'},
    {'url': 'clubes/2018/40/1/sdr-pedrea/plantilla', 'name': 'SDR PEDRENA'},
    {'url': 'clubes/2018/102/1/portugalete/plantilla', 'name': 'PORTUGALETE'},
    {'url': 'clubes/2018/3/1/san-juan-sumelec/plantilla', 'name': 'SAN JUAN-SUMELEC'},
    {'url': 'clubes/2018/16/1/zarautz-babyauto/plantilla', 'name': 'ZARAUTZ-BABYAUTO'},
    {'url': 'clubes/2018/17/1/zumaia-salegi-jatetxea/plantilla', 'name': 'ZUMAIA-SALEGI JATETXEA'}
  ]

  def get_main_page(self):
    main_page = requests.get(f'{self.url_base}clubes')
    with open('./liga-arc.html', 'w', encoding='utf-8') as f:
      f.write(main_page.text)
    f.close()

  def get_club_data(self, club, url):
    print(f'Getting data for {club}: {self.url_base}{url}')
    page = requests.get(f'{self.url_base}{url}')
    with open(f'{self.file_path}/{club}.html', 'w', encoding='utf-8') as f:
      f.write(page.text)
    f.close()

  def get_rowers_data(self, club):
    with open(f'{self.file_path}/{club}.html', 'r', encoding='utf-8') as f:
      document = lxml.html.fromstring(f.read())
      links = document.cssselect('.ver-ficha a')
      for link in links:
        link_lst = link.get('href').split('/')
        rower_name = link_lst[-1:]
        print(f'Getting data for {club} {rower_name}')
        page = requests.get(link.get('href'))
        with open(f'{self.file_path}/{club}-{rower_name}.html', 'w', encoding='utf-8') as f2:
          f2.write(page.text)
        continue
    f.close()


  def parse_rower_data(self, content):
    name = ''
    name = content.cssselect('.nombre')[0].text.strip()
    age = int(content.cssselect('.edad strong')[0].text.strip())
    print(f'{name} {age}')
    return (name, age)

  def analize_staff_data(self, data):
    ages = []
    for d in data:
      age = d[1]
      ages.append(age)
    average = sum(ages)/len(ages)
    return average

  def isRower(self, content):
    title = content.cssselect('.fizda')
    if title[0].text.strip() == 'Remero':
      return True
    else:
      return False

  def parse_staff_data(self, club):
    staff_data = []
    print(club)
    for pathname in glob.glob(f'./{self.file_path}/{club}-*'):
      try:
        with open(pathname, 'r', encoding='utf-8') as f:
          document = lxml.html.fromstring(f.read())

          data = self.parse_rower_data(document)
        staff_data.append(data)
      except IndexError:
        pass
    return self.analize_staff_data(staff_data)

  def analize(self):
    for club in self.staff:
        average = self.parse_staff_data(club['name'])
        print(f'{club["name"]}: {average}')
        print(10*'-')

  def __init__(self):
    pass