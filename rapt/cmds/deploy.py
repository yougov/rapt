import sys
import click

from rapt.connection import get_vr
from rapt.util import edit_yaml, dump_yaml, load_yaml
from rapt.models import query
from rapt.events import filtered_events
from rapt.codes import RESOURCE_MISSING


def get_release(config, vr):
    # We need to make sure we have the release
    results = query('Release', vr, {'compiled_name': config['release']})
    if not results:
        click.echo('%s is not a valid release name' % config['release'])
        sys.exit(RESOURCE_MISSING)
    return results.pop()


@click.command()
@click.argument('deploy_config', type=click.File('rb'), nargs=-1)
@click.option('--release', '-r', help='The release of the app to deploy')
@click.option('--proc', '-p', help='The proc to deploy')
@click.option('--config-name', '-c', help='The config name to deploy')
@click.option('--hostname', '-H', help='The hostname to deploy to')
@click.option('--port', '-P', help='The port to deploy to')
def deploy(build_config, app_name, release, proc, config_name, hostname, port):
    """Trigger new a build.

    The `build_config` is a YAML file with the require fields
    necessary to do the build. If no build_config is provided, your
    $EDITOR will be opened with a template that can be used to
    configure the build.
    """
    tmpl = {
        'release': release or '',
        'proc': proc or '',
        'config_name': config_name or '',
        'hostname': hostname or '',
        'port': port or '',
    }
    vr = get_vr()

    # Do we use some pre-canned yaml?
    if build_config:
        config = load_yaml(build_config[0])

    # How about some command line flags
    elif release and proc and config_name and hostname:
        config = tmpl

    # No? We'll use our template and editor
    else:
        config = edit_yaml(dump_yaml(tmpl))

    # We have a config so we'll actually do stuff
    if config:
        release = get_release(config, vr)

        # TODO: Get VR returning some value.
        release.deploy(config['hostname'],
                       config['port'],
                       config['proc'],
                       config['config_name'])

        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(vr, forever=True):
            click.echo(event)
