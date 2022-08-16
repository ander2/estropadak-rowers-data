''' Export analyzed data as JSON '''

import click
import pickle
import datetime
import json
import logging
from .calculate_alta_baja import calculate_alta_baja

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('estropadak')
logger.setLevel('DEBUG')
db = None


def get_data(liga):
    ''' Load serialized data '''
    data = None
    with open(f'./results/{liga.lower()}_data', 'rb') as f:
        data = pickle.load(f)
    return data


def update_stats(year, liga, stats):
    ''' Update couch object '''
    global db
    doc_id = f'rank_{liga.upper()}_{year}'
    doc = db[doc_id]
    for team, data in stats[year].items():
        doc['stats'][team].update(data)
    db[doc_id] = doc


def encode_rower(r):
    if hasattr(r, 'name'):
        return {
            "name": r.name,
            "birthday": r.birthday,
            "birthplace": r.birthplace,
            "historial": r.historial
        }
    else:
        return r


def create_team_page(year, liga, teams):
    ''' Create couch object to store the team'''
    global db
    for team, data in teams.items():
        key = f'team_{liga.upper()}_{year}_{team}'
        doc = {
            "name": team,
            "year": year,
            "liga": liga.upper()
        }
        doc['rowers'] = json.loads(
            json.dumps(data, default=encode_rower, indent=2)
        )
        try:
            old_doc = db[key]
            doc['_rev'] = old_doc.rev
            db[key] = doc
        except:
            db[key] = doc


def calculate_rowers_ages(rowers, base_year, liga, age_correction=0):
    ages = []
    start = datetime.datetime.strptime(f'01-06-{base_year}', '%d-%m-%Y')
    for rower in rowers:
        age = 0
        if liga == 'ACT' or liga == 'EUSKOTREN':
            birthday = datetime.datetime.strptime(
                rower.birthday,
                '%d-%m-%Y')
            d = start - birthday
            age = d.days / 365
        else:
            if rower.age:
                age = rower.age
        if age_correction > 0:
            logger.debug(f'Applying age correction of {age_correction}')
            age = age - age_correction
        if age > 0:
            ages.append(age)
    return ages


@click.command()
@click.option("--liga", type=click.Choice(['ACT', 'ARC1', 'ARC2', 'EUSKOTREN', 'ETE']))
@click.option("--year", type=click.INT, help="Year to export")
@click.option("--age_correction", type=click.INT, help="Age correction for ARC leagues", default=0)
def export(liga, year, age_correction):
    year_to_export = year
    if liga:
        ligak = [liga]
    else:
        ligak = ['ACT', 'ARC1', 'ARC2', 'EUSKOTREN', 'ETE']
    for liga in ligak:
        data = get_data(liga)
        update_aldaketak = True
        result = {}
        for year, teams in data.items():
            if year_to_export and year != year_to_export:
                continue
            result[year] = {}
            for team, rowers in teams.items():
                logger.info(f'**{team}**')
                alta = {}
                baja = {}
                try:
                    alta, baja = calculate_alta_baja(
                        teams,
                        data[year - 1],
                        team)
                    update_aldaketak = True
                    result[year][team] = {
                        "rowers": {
                            "altak": len(alta),
                            "bajak": len(baja)
                        }
                    }
                except KeyError as e:
                    update_aldaketak = False
                    logger.debug(f'{team} not found on {year-1}')
                    logger.exception(e)
                ages = calculate_rowers_ages(rowers, year, liga, age_correction=age_correction)
                if len(ages) > 0:
                    min_age = min(ages)
                    max_age = max(ages)
                    avg_age = sum(ages) / len(ages)
                else:
                    min_age = 0
                    max_age = 0
                    avg_age = 0
                try:
                    result[year][team].update({
                        "age": {
                            "min_age": min_age,
                            "max_age": max_age,
                            "avg_age": avg_age
                        }
                    })
                except KeyError:
                    result[year][team] = {
                        "age": {
                            "min_age": min_age,
                            "max_age": max_age,
                            "avg_age": avg_age
                        }
                    }

            print(json.dumps(result))


if __name__ == "__main__":
    export()
