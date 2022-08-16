# Arraunlari datuen parserra
Arraunlari datuak eskuratu, parseatu eta tratatzen dituen komando multzoa.

## Erabilera
```
$ python3 index.py fetch-contents 2022 act
$ python3 index.py analize act --year=2022
$ python3 index.py export --liga=ACT --year=2022
````

3 komando daude eskuragarri:

* `fetch-contents`: pasatzen zaizkion urte eta ligako talde eta arraunlarien
web orriak eskuratu eta gordetzen ditu.
* `analize`: pasatzen zaizkion liga eta urte edo urte tarteko web orriak irakurri
eta datu egituratuak dituen fitxategi bat sortzen du.
* `export`: aurreko pausuan sortu berri den fitxategitik guk esandako liga eta urteko
datuak, JSON formatuan exportatzen ditu.

## Oharrak

Taldeetan egon diren arraunlari alta/bajak kalkulatu ahal izateko, aurreko urteko datuak
kargatuta egon behar dira, beraz, sekuentzialki egin beharreko lan bat da.



## Parsers
Liga bakoitzak, bere parserra dauka, dagokion karpetaren barruan.

# Parser for rower data

## Usage
```
$ python3 index.py fetch-contents 2022 act
$ python3 index.py analize act --year=2022
$ python3 index.py export --liga=ACT --year=2022
```



## Parsers
Every league has it's own parser located in the parser folder