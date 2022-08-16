import click

from parsers.actageparser import ActAgeParser
from parsers.arc1ageparser import Arc1AgeParser
from parsers.arc2ageparser import Arc2AgeParser
from parsers.euskotrenageparser import EuskotrenAgeParser
from parsers.eteageparser import EteAgeParser
from utils.export_data import export
from utils.analize import analize


@click.command()
@click.argument('year', type=click.INT, required=True)
@click.argument(
    'league',
    type=click.Choice([
        'act', 'arc1', 'arc2', 'euskotren', 'ete'
    ]), required=True)
def fetch_contents(year, league):
    ''' Fetch page content related to rowing clubs and rowers '''
    if league == 'act':
        parser = ActAgeParser()
    elif league == 'arc1':
        parser = Arc1AgeParser()
    elif league == 'arc2':
        parser = Arc2AgeParser()
    elif league == 'euskotren':
        parser = EuskotrenAgeParser()
    elif league == 'ete':
        parser = EteAgeParser()
    parser.staff = parser.get_clubs_in_year(year, league)
    for club in parser.staff:
        print(f'Fetching contens for {club["name"]} in {club["url"]}')
        parser.fetch_plantilla_page(club['name'], year, club['url'])
        parser.fetch_rower_pages(club['name'], year)


@click.group()
def cli():
    pass


cli.add_command(fetch_contents)
cli.add_command(analize)
cli.add_command(export)

if __name__ == '__main__':
    cli()
