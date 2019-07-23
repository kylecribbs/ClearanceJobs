#Maybe add CLI in the future...
import os

import yaml
import click
from . import ClearanceJobs

ENV = os.environ

@click.command()
@click.option(
    '--username',
    default=ENV.get('CLEARANCEJOB_USERNAME', ''),
    show_default='CLEARANCEJOB_USERNAME env variable'
)
@click.option(
    '--password',
    default=ENV.get('CLEARANCEJOB_PASSWORD', ''),
    show_default='CLEARANCEJOB_PASSWORD env variable'
)
@click.option(
    '--sql-url',
    default=ENV.get('CLEARANCEJOB_SQLURL', ''),
    show_default='CLEARANCEJOB_SQLURL env variable'
)
@click.option(
    '--api-url',
    default='https://api.clearancejobs.com/api/v1',
    show_default='https://api.clearancejobs.com/api/v1'
)
@click.option("--creds", type=click.Path())
def cli(*args, **kwargs):
    """ClearanceJobs CLI for dumiies.

    Credentials ingestion are in the following order:
    \b

    Creds YAML > CLI Flag > Environmental Variable
    """
    if kwargs['creds']:
        credentials = ""
    cj = ClearanceJobs(
        kwargs['username'],
        kwargs['password'],
        kwargs['api_url']
    )
