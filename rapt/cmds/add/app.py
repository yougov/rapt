import click

from rapt.connection import get_vr
from rapt.models import apps, models
from rapt.util import edit_yaml, dump_yaml

from pprint import pformat


def validate(app_config):
    vcs = ['git', 'hg']

    repo_type = app_config['repo_type']

    if not isinstance(repo_type, basestring):
        repo_type = repo_type[0]

    assert repo_type in vcs

    app_config['repo_type'] = repo_type

    return app_config


@click.command()
def app():
    tmpl = {
        'name': '',
        'repo': '',
        'repo_type': [
            'git', 'hg',
        ],
    }

    vr = get_vr()

    info = {
        'current_apps': [app['name'] for app in apps(vr)],
    }

    config = edit_yaml(dump_yaml(tmpl), dump_yaml(info))

    config = validate(config)
    click.echo('Creating new app with the following config:')
    click.echo(pformat(config))
    click.echo()

    if click.confirm('Add app?'):
        app = models.App(vr, config)
        app.create()
        click.echo('Added %s!' % app.name)
