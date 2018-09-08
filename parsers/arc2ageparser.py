from parsers.arc1ageparser import Arc1AgeParser

class Arc2AgeParser(Arc1AgeParser):
  url_base = 'http://www.liga-arc.com/es/'
  file_path = './pages/arc2'
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
      {'url': 'clubes/2018/92/1/bermeo-sumoil/plantilla', 'name': 'BERMEO-SUMOIL'},
      {'url': 'clubes/2018/91/1/elantxobe-idar/plantilla', 'name': 'ELANTXOBE-IDAR'},
      {'url': 'clubes/2018/31/1/camargo/plantilla', 'name': 'CAMARGO'},
      {'url': 'clubes/2018/28/1/castrea/plantilla', 'name': 'Castreña'},
      {'url': 'clubes/2018/29/1/colindres/plantilla', 'name': 'Colindres'},
      {'url': 'clubes/2018/39/1/laredo-la-pejinuca/plantilla', 'name': 'LAREDO-LA PEJINUCA'},
      {'url': 'clubes/2018/12/1/donostiarra/plantilla', 'name': 'DONOSTIARRA'},
      {'url': 'clubes/2018/96/1/getxo/plantilla', 'name': 'Getxo'},
      {'url': 'clubes/2018/1/1/hondarribia/plantilla', 'name': 'HONDARRIBIA'},
      {'url': 'clubes/2018/98/1/lutxana-ae/plantilla', 'name': 'LUTXANA AE'},
      {'url': 'clubes/2018/18/1/mutriku/plantilla', 'name': 'MUTRIKU'},
      {'url': 'clubes/2018/14/1/orio-babyauto/plantilla', 'name': 'ORIO-BABYAUTO'},
      {'url': 'clubes/2018/4/1/san-pedro/plantilla', 'name': 'SAN PEDRO'},
      {'url': 'clubes/2018/37/1/irc-santoa/plantilla', 'name': 'IRC SANTOÑA'},
  ]

def __init__(self):
  super()