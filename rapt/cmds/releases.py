import click

from rapt.connection import get_vr
from rapt.models import query


@click.command()
@click.option('--app-name', '-a')
@click.option('--limit', '-l', default=20)
def releases(app_name, limit):
    """List releases and print the compiled name.

    The `compiled_name` includes the app, build version and app hash.
    """
    vr = get_vr()

    q = {
        'build__app__name': app_name,
    }

    # add filters if we need to be...
    for i, release in enumerate(query('Release', vr, q)):
        click.echo(release.compiled_name)
        if i == limit:
            return
