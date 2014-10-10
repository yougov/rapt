import os

import click

from .connection import get_vr

from .events import filtered_events
from .cmds.swarm import swarm
from .cmds.swarms import swarms
from .cmds.add import add
from .cmds.releases import releases
from .cmds.build import build
from .cmds.builds import builds

from pprint import pformat


@click.command()
def event_stream():
    """Tail the event stream.

    This will print the time, title, tags and any other top level keys
    other than message. If event has an error tag ('failed',
    'failure'), the message will be printed as well."""

    vr = get_vr()
    for event in filtered_events(vr, forever=True):
        click.echo(event)


@click.command()
def info():
    """Find the url / username that rapt will be using.

    Rapt can use the `VELOCIRAPTOR_URL` and `VELOCIRAPTOR_USERNAME`
    environment variables to configure commands. The info command will
    print these out for you and try connecting to the API to help
    confirm things are set up correctly."""

    vr = get_vr()

    click.echo('The Velociraptor URL I have on file is %s' % vr.base)
    click.echo('Youre username is %s' % vr.username)
    url = vr._build_url('/api/v1/')
    resp = None
    try:
        resp = vr.session.head(url)
    except Exception as e:
        pass

    if resp and resp.ok:
        click.echo('I made a request to the API and things look good!')
    else:
        click.echo('Hmm... We had some trouble contacting the API.')
        click.echo('Here is some traceback from the response:')
        click.echo()

        if not resp and e:
            raise e
        else:
            click.echo('Request: HEAD %s' % resp.request.url)
            click.echo('Headers: %s' % pformat(dict(resp.headers)))
            click.echo('Content: %s' % resp.content)
            click.echo()

            resp.raise_for_status()


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
rapt.add_command(releases)
rapt.add_command(build)
rapt.add_command(builds)
rapt.add_command(add)

rapt.add_command(event_stream)
rapt.add_command(info)
# rapt.add_command(test)

if __name__ == '__main__':
    rapt()
