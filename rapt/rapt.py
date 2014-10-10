import os

import click

from .connection import get_vr

from .events import filtered_events
from .cmds.swarm import swarm
from .cmds.swarms import swarms
from .cmds.add import add
from .cmds.releases import releases
from .cmds.build import build


@click.command()
def event_stream():
    """Tail the event stream.

    This will print the time, title, tags and any other top level keys
    other than message. If event has an error tag ('failed',
    'failure'), the message will be printed as well."""

    vr = get_vr()
    for event in filtered_events(vr, forever=True):
        click.echo(event)


@click.group()
@click.option('--username', '-u', help='Velociraptor Username')
@click.option('--host', '-H', help='The Velociraptor URL')
def rapt(username, host):
    """Rapt! The velociraptor command line tool."""

    if username:
        os.environ['VELOCIRAPTOR_USERNAME'] = username
    if host:
        os.environ['VELOCIRAPTOR_URL'] = host


rapt.add_command(swarms)
rapt.add_command(swarm)
rapt.add_command(event_stream)
rapt.add_command(add)
rapt.add_command(releases)
rapt.add_command(build)
# rapt.add_command(test)

if __name__ == '__main__':
    rapt()
