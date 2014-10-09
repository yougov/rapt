import click

from rapt.connection import get_vr
from rapt.models import apps
from rapt.util import edit_yaml, dump_yaml


@click.command()
def swarm():
    """Add a new swarm."""
    vr = get_vr()

    tmpl = {
        'app_name': '',
        'version': '',
        'proc_name': '',
        'size': '',
        'squad': ''
    }

    info = {
        'available apps': [app['name'] for app in apps(vr)],
    }

    footer = dump_yaml(info)
    config = edit_yaml(dump_yaml(tmpl), footer)
    print(config)
