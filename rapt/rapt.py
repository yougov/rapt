import sys
import yaml

import click

from vr.common.models import Swarm

from .connection import get_vr
from .events import SwarmEvents, filtered_events


class StdInOrStringList(click.ParamType):
    name = 'string'

    def gen(self, src):
        for line in src:
            yield line.strip()

    def convert(self, value, param, ctx):
        if value == '-':
            return [name for name in self.gen(sys.stdin)]
        return value


@click.command()
@click.option('--app-name', '-a')
@click.option('--config-name', '-c')
@click.option('--proc-name', '-p')
def swarms(app_name, config_name, proc_name):
    vr = get_vr()
    if not app_name:
        swarms = Swarm.load_all(vr)
        for swarm in swarms:
            click.echo(swarm.name)
    else:
        query = {
            'app__name': app_name,
            'config_name': config_name,
            'proc_name': proc_name,
        }

        query = {k: v for k, v in query.items() if v}

        results = vr.query(Swarm.base, query)
        for doc in results['objects']:
            swarm = Swarm(vr, doc)
            click.echo(swarm.name)


def dump_yaml(obj):
    return yaml.dump(obj, default_flow_style=False)


def edit_yaml(content='', footer=''):
    MARKER = '# Everything below is ignored\n\n'
    message = click.edit(content + '\n\n' + MARKER + footer,
                         extension='.yaml')
    if message is not None:
        yaml_content = message.split(MARKER, 1)[0].rstrip('\n')
        return yaml.safe_load(yaml_content)


@click.command()
@click.argument('names', type=StdInOrStringList(), nargs=-1)
def swarm(names):
    vr = get_vr()
    print(names)
    swarms = [Swarm.by_name(vr, name) for name in names]

    # collect config
    configs = {
        swarm.name: {
            'version': str(swarm.version),
            'size': str(swarm.size)
        }
        for swarm in swarms
    }

    config = edit_yaml(dump_yaml(configs.values()[0]),
                       footer=dump_yaml(configs))

    if config:
        click.echo('Updating swarms with: %s' % config)

        event_handlers = []

        for swarm in swarms:
            swarm.dispatch(**config)
            event_handlers.append(SwarmEvents(swarm, vr))
            click.echo('Swarmed %s!' % swarm.name)

        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(event_handlers, vr):
            click.echo(event)


@click.command()
def event_stream():
    vr = get_vr()
    for event in filtered_events(vr):
        click.echo(event)


@click.group()
def rapt():
    pass


rapt.add_command(swarms)
rapt.add_command(swarm)
rapt.add_command(event_stream)
# rapt.add_command(test)

if __name__ == '__main__':
    rapt()
