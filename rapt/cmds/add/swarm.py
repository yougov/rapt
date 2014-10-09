import click

from rapt.connection import get_vr
from rapt.models import apps, squads, models
from rapt.util import edit_yaml, dump_yaml, load_yaml

from pprint import pformat


def validate_uri(name_or_uri, objs):
    uris = set([s['resource_uri'] for s in objs])
    names = {s['name']: s['resource_uri'] for s in objs}

    if name_or_uri in names:
        return names[name_or_uri]
    assert name_or_uri in uris
    return name_or_uri


def validate(config, squads, apps):
    config['squad'] = validate_uri(config['squad'], squads)
    config['app'] = validate_uri(config['app'], apps)

    if 'os_image' not in config:
        config['os_image'] = None
    return config


def get_config(vr, app_list, squad_list):
    tmpl = {
        'app': '',
        'version': '',
        'proc_name': '',
        'size': '',
        'squad': '',
        # TODO: Add config options
    }

    info = {
        'NOTES': 'Use the URL when copying vlaues.',

        'available apps': {
            str(app['name']): str(app['resource_uri'])
            for app in app_list
        },

        'available squads': {
            str(squad['name']): str(squad['resource_uri'])
            for squad in squad_list
        },
    }

    footer = dump_yaml(info)
    return edit_yaml(dump_yaml(tmpl), footer)


@click.command()
@click.argument('config', type=click.File('rb'), nargs=-1)
def swarm(config):
    """Add a new swarm."""
    vr = get_vr()

    app_list = apps(vr)
    squad_list = squads(vr)

    if config:
        config = load_yaml(config[0])

    config = config or get_config(vr, app_list, squad_list)

    if config:
        config = validate(config, squad_list, app_list)
        click.echo('Creating swarm with following config:\n\n')
        click.echo(dump_yaml(config))
        click.echo()
        click.echo()

        if click.confirm('Add the swarm?', default=True):
            swarm = models.Swarm(vr, config)
            swarm.create()
            click.echo('Swarm %s created!' % (swarm.name))
