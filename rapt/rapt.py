import click

from .connection import get_vr

from .events import filtered_events
from .cmds.swarm import swarm
from .cmds.swarms import swarms


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
