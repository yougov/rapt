import sys
import pdb
import yaml

import click

from vr.common.models import Swarm

from .connection import get_vr


class StdInOrStringList(click.ParamType):
    name = 'string'

    def gen(self, src):
        for line in src:
            yield line.strip()

    def convert(self, value, param, ctx):
        if value == '-':
            return self.gen(sys.stdin)
        return [value]


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


def edit_yaml(content=''):
    MARKER = '# Everything below is ignored\n'
    message = click.edit(content + '\n\n' + MARKER,
                         extension='.yaml')
    if message is not None:
        yaml_content = message.split(MARKER, 1)[0].rstrip('\n')
        return yaml.safe_load(yaml_content)


@click.command()
@click.argument('names', type=StdInOrStringList(), nargs=-1)
def swarm(names):
    vr = get_vr()
    if names:
        names = names[0]

    for name in names:
        swarm = Swarm.by_name(vr, name)
        current_config = {
            'version': str(swarm.version),
            'size': str(swarm.size)
        }
        config = edit_yaml(yaml.dump(current_config, default_flow_style=False))
        if config:
            click.echo('Got config: %s' % config)


@click.group()
def rapt():
    pass


rapt.add_command(swarms)
rapt.add_command(swarm)

if __name__ == '__main__':
    rapt()
