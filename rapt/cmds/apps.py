import click

from rapt.connection import get_vr
from rapt.models import query


@click.command()
def apps():
    """List apps."""

    vr = get_vr()

    # add filters if we need to be...
    for i, app in enumerate(query('App', vr)):
        click.echo(app.name)
