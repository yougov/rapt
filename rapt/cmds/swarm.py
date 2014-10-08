from collections import namedtuple

import click

from vr.common.models import Swarm

from ..util import stdin, edit_yaml, dump_yaml
from ..events import SwarmEvents, filtered_events
from ..connection import get_vr


SwarmInfo = namedtuple('SwarmInfo', ['name', 'obj', 'config', 'handlers'])


def swarm_event_handler(swarm, username):
    return SwarmEvents(swarm.app_name,
                       swarm.version,
                       swarm.proc_name,
                       username)


def load_swarms(vr, names):
    """Return an ordered of swarms."""
    swarms = []
    for name in names:
        swarm = Swarm.by_name(vr, name)
        handlers = swarm_event_handler(swarm, vr.username)
        swarms.append(SwarmInfo(name, swarm, swarm_config(swarm), handlers))
    return swarms


def swarm_config(swarm):
    """Create a dict of things you can edit when swarming"""
    return {
        'version': str(swarm.version),
        'size': str(swarm.size)
    }


@click.command()
@click.argument('names', nargs=-1)
@click.option('--dry-run', is_flag=True, default=False)
def swarm(names, dry_run):
    vr = get_vr()
    swarms = load_swarms(vr, names or stdin())
    configs = {swarm.name: swarm.config for swarm in swarms}
    if not configs:
        click.echo('No configs found')
        return

    new_config = edit_yaml(dump_yaml(configs))

    if not new_config:
        click.echo('No changes to the config. Exiting...')
        return

    event_handlers = []

    for swarm in swarms:
        config = new_config[swarm.name]
        if config != swarm.config:
            click.echo('Updating swarms with: %s' % config)
            if not dry_run:
                swarm.dispatch(**config)
            click.echo('Adding swarm event handlers: %s' % swarm.handlers)
            event_handlers.append(swarm.handlers)
            click.echo('Swarmed %s!' % swarm.name)

    if event_handlers:
        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(vr, event_handlers):
            click.echo(event)
