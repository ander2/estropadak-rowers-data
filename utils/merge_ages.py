''' Recovers stats from API and merges age and rower related data '''
import sys
import requests
import json


liga = sys.argv[1]
year = sys.argv[2]

url = f'http://www.estropadak.eus/api/sailkapenak/rank_{liga}_{year}'
r = requests.get(url)
sailkapenak = r.json()
sailkapen_eguneratuak = sailkapenak

adinak = None
with open(f'./results/ages_{liga.lower()}.json', 'r') as f:
    adinak = json.load(f)

if adinak:
    for team in sailkapenak['stats']:
        team['value']['age'] = adinak[year][team['name']]['age']
        team['value']['rowers'] = adinak[year][team['name']]['rowers']

with open(f'./rank_{liga}_{year}', 'w') as f:
    json.dump(sailkapenak, f, indent=2)
