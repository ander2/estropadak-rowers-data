'''
Fix rowers age, as they are calculated related to
the current year when accessing the html pages
'''
import click
import pickle


def load_data(liga):
    ''' Load serialized data '''
    data = None
    with open(f'./results/{liga.lower()}_data', 'rb') as f:
        data = pickle.load(f)
    return data


def save_data(liga: str, data):
    with open(f'./results/{liga}_data', 'wb') as f:
        pickle.dump(data, f)


@click.command()
@click.option('--year', type=click.INT, help='Year of the pages')
@click.argument(
    'liga',
    type=click.Choice([
        'arc1', 'arc2'
    ]))
def fix_ages(liga, year):
    data = load_data(liga)
    for urtea, taldeak in data.items():
        if urtea == 2020:
            continue
        print('"'*10 + f'{urtea}' + '"'*10)
        offset = year - urtea
        for team, rowers in taldeak.items():
            print(f'>>>>>{team}')
            for rower in rowers:
                if rower.age is not None:
                    fixed_age = rower.age - offset
                    rower.age = fixed_age
                    print(f'{rower.name}\t{fixed_age}')
    save_data(liga, data)


if __name__ == "__main__":
    fix_ages()
