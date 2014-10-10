import click

from rapt.connection import get_vr
from rapt.models import query, models
from rapt.util import edit_yaml, dump_yaml

from pprint import pformat


@click.command()
def buildpack():
    tmpl = {
        'repo_url': '',
        'repo_type': ['git', 'hg'],
        'description': '',
        'order': 0,
    }

    vr = get_vr()

    info = {
        'available buildpacks': [
            bp.repo_url for bp in query('buildpack', vr)
        ]
    }

    config = edit_yaml(dump_yaml(tmpl),
                       dump_yaml(info))

    click.echo('Creating buildpack with following config:\n')
    click.echo(pformat(config))
    click.echo()

    if click.confirm('Create buildpack?'):
        bp = models.Buildpack(vr, config)
        bp.create()
        click.echo('Create %s %s!' % (bp.repo_url, bp.resource_uri))
