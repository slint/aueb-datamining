from datetime import datetime, timedelta
from functools import partial
from sqlalchemy_utils import create_database, database_exists, drop_database

import click
from click_datetime import Datetime

from politically_correct.tasks import harvest, categorize
from politically_correct.models import create_tables
from politically_correct.config import cfg

# Pimp my `click.secho` with color shortcuts
for color in ('green', 'blue', 'yellow', 'red', 'magenta', 'cyan'):
    setattr(click, '%secho' % color[0], partial(click.secho, fg=color))


@click.group('politically-correct')
def cli():
    pass


@cli.command('harvest')
@click.option('--hashtag', '-h', multiple=True, help='Hashtags to search for.')
@click.option('--mention', '-m', multiple=True, help='Mentions to search for.')
@click.option('--since', '-s',
              type=Datetime(format='%Y-%m-%d'),
              default=lambda: datetime.now() - timedelta(15),
              help='Hashtags to search for.')
@click.option('--place', '-p', help='Place to search for.')
def _harvest(hashtag, mention, since, place):
    harvest(hashtag, mention, since, place)


@cli.command('categorize')
def _categorize():
    categorize()


@cli.group('db')
def db():
    pass


@db.command('create')
def create_db():
    click.becho('Database [%s]' % cfg.DATABASE_URL)
    if database_exists(cfg.DATABASE_URL):
        click.yecho('Database already exists...')
        click.confirm('Drop and create new?', default=False, abort=True)
        click.recho('Dropping database...')
        drop_database(cfg.DATABASE_URL)
        click.recho('Database dropped!')
    click.becho('Creating new database...')
    create_database(cfg.DATABASE_URL)
    click.gecho('Database created!')

    click.becho('Creating database tables...')
    create_tables()
    click.gecho('Tables created!')


if __name__ == '__main__':
    cli()
