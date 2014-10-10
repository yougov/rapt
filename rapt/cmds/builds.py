import click

from rapt.connection import get_vr
from rapt.models import query


@click.command()
@click.option('--app-name', '-a')
@click.option('--limit', '-l', default=20)
def builds(app_name, limit):
    """List builds.
    """
    vr = get_vr()

    q = {
        'app__name': app_name,
    }

    # add filters if we need to be...
    for i, build in enumerate(query('Build', vr, q)):
        if not build.file:
            click.echo('[failed] %s %s' % (build.resource_uri, build.app))
        else:
            click.echo(build.file)
        if i == limit:
            return
