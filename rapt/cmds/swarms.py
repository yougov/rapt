import click

from vr.common.models import Swarm

from ..connection import get_vr


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
            'app__name__icontains': app_name,
            'config_name': config_name,
            'proc_name': proc_name,
        }

        query = {k: v for k, v in query.items() if v}

        results = vr.query(Swarm.base, query)
        for doc in results['objects']:
            swarm = Swarm(vr, doc)
            click.echo(swarm.name)
