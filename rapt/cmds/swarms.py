import click

from rapt.models import query
from rapt.connection import get_vr


@click.command()
@click.option('--app-name', '-a')
@click.option('--config-name', '-c')
@click.option('--proc-name', '-p')
def swarms(app_name, config_name, proc_name):
    vr = get_vr()
    if not app_name:
        swarms = query('Swarm', vr)
        for swarm in swarms:
            click.echo(swarm.name)
    else:
        q = {
            'app__name__icontains': app_name,
            'config_name': config_name,
            'proc_name': proc_name,
        }

        q = {k: v for k, v in q.items() if v}

        for swarm in query('Swarm', vr, q):
            click.echo(swarm.name)
