import os

import click

from .connection import get_vr

from .events import filtered_events
from .cmds.swarm import swarm
from .cmds.swarms import swarms


@click.command()
def event_stream():
    vr = get_vr()
    for event in filtered_events(vr, forever=True):
        click.echo(event)


@click.group()
@click.option('--username', '-u')
@click.option('--password', '-p')
def rapt(username, password):
    if username:
        os.environ['VELOCIRAPTOR_USERNAME'] = username
    if password:
        os.environ['VELOCIRAPTOR_PASSWORD'] = password


rapt.add_command(swarms)
rapt.add_command(swarm)
rapt.add_command(event_stream)
# rapt.add_command(test)

if __name__ == '__main__':
    rapt()
