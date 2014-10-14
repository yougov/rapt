import sys

from collections import namedtuple

import click

from rapt.models import query
from rapt.util import stdin, edit_yaml, dump_yaml
from rapt.events import SwarmEvents, filtered_events
from rapt.connection import get_vr


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
        try:
            app_name, config_name, proc_name = name.split('-')
        except ValueError:
            click.echo('Invalid swarm name %s' % name)
            sys.exit(3)

        q= {
            'app_name': name,
            'config_name': config_name,
            'proc_name': proc_name
        }

        swarm = query('Swarm', vr, q).next()
        handlers = swarm_event_handler(swarm, vr.username)
        swarms.append(SwarmInfo(name, swarm, swarm_config(swarm), handlers))
    return swarms


def swarm_config(swarm):
    """Create a dict of things you can edit when swarming"""
    return {
        'version': str(swarm.version),
        'size': str(swarm.size)
    }


def swarm_id_handler(swarm_id):
    def handler(event):
        if 'swarm_id' in event and event['swarm_id'] == swarm_id:
            return event
    return handler


@click.command()
@click.argument('names', nargs=-1)
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not actually reswarm anything.')
def swarm(names, dry_run):
    """Swarm an existing swarm.

    The swarm command allows swarming more than one swarm as defined
    by the `names` argument. The names can be passed directly in the
    command.

      $ rapt swarm myapp-production-web myapp-production-workers

    The `names` can also be passed in via stdin. For eaxmple:

      $ rapt swarms | grep myapp | rapt swarm

    This will open a YAML file where each swarm's settings can be
    edited. Only those swarms that have been edited will be reswarmed.

    After the swarms have been triggered, the events for those swarms
    will be printed. The script will exit when the events have
    finished or there has been a failure in one of swarms.
    """
    vr = get_vr()
    swarms = load_swarms(vr, names or stdin())
    configs = {str(swarm.name): swarm.config for swarm in swarms}
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
                doc = swarm.obj.dispatch(**config)
                event_handlers.append(swarm_id_handler(doc['swarm_id']))
            click.echo('Swarmed %s!' % swarm.name)

    if event_handlers:
        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(vr, event_handlers):
            click.echo(event)


@click.command()
@click.argument('names', nargs=-1)
@click.option('--dry-run', is_flag=True, default=False,
              help='Do not actually reswarm anything.')
def reswarm(names, dry_run):
    """Reswarm a swarm without editing the config."""
    vr = get_vr()
    swarms = load_swarms(vr, names or stdin())

    event_handlers = []

    for swarm in swarms:
        click.echo('Running swarm %s with: %s' % (swarm.name, swarm.config))
        if not dry_run:
            doc = swarm.obj.dispatch(**swarm.config)
            event_handlers.append(swarm_id_handler(doc['swarm_id']))
        click.echo('Swarmed %s!' % swarm.name)

    if event_handlers:
        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(vr, event_handlers):
            click.echo(event)
