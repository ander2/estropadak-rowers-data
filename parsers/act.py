import requests
import lxml.html

class ActAgeParser:
  url_base = 'http://euskolabelliga.com'
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
    {"url": "/clubes/plantilla.php?id=es&c=2", "name": "cabo"},
    {"url": "/clubes/plantilla.php?id=es&c=4", "name": "tiran"},
    {"url": "/clubes/plantilla.php?id=es&c=8", "name": "hondarribia"},
    {"url": "/clubes/plantilla.php?id=es&c=9", "name": "orio"},
    {"url": "/clubes/plantilla.php?id=es&c=38", "name": "kaiku"},
    {"url": "/clubes/plantilla.php?id=es&c=46", "name": "ondarroa"},
    {"url": "/clubes/plantilla.php?id=es&c=94", "name": "donostiarra"},
    {"url": "/clubes/plantilla.php?id=es&c=11", "name": "sanjuan"},
    {"url": "/clubes/plantilla.php?id=es&c=18", "name": "sanpedro"},
    {"url": "/clubes/plantilla.php?id=es&c=37", "name": "santurtzi"},
    {"url": "/clubes/plantilla.php?id=es&c=13", "name": "urdaibai"},
    {"url": "/clubes/plantilla.php?id=es&c=68", "name": "zierbena"},
  ]

  def get_main_page(self):
    main_page = requests.get(self.url_base)
    with open('./pages/euskolabel.html', 'w', encoding='utf-8') as f:
      f.write(main_page.text)

    f.close()

  def get_club_data(self, club, url):
    print(f'Getting data for {club}: {self.url_base}{url}')
    page = requests.get(f'{self.url_base}{url}')
    with open(f'./pages/{club}.html', 'w', encoding='utf-8') as f:
      f.write(page.text)
    f.close()

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

  def isRower(self, content):
    title = content.cssselect('.fizda')
    if title[0].text.strip() == 'Remero':
      return True
    else:
      return False

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

  def analize(self):
    for club in self.clubs:
      with open(f'./pages/{club["name"]}.html', 'r', encoding='utf-8') as f:
        average = self.parse_staff_data(f.read())
        print(f'{club["name"]}: {average}')
        print(10*'-')
      f.close()

  def __init__(self):
    pass