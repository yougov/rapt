import click

from rapt.connection import get_vr
from rapt.util import edit_yaml, dump_yaml, load_yaml
from rapt.models import query, models
from rapt.events import filtered_events


def validate(config, apps, images):
    apps = {app.name: app.resource_uri for app in apps}

    if config['app'] not in apps.values():
        config['app'] = apps[config['app']]

    if 'os_image' not in config or not config['os_image']:
        config['os_image'] = list(images)[0].resource_uri

    return config


@click.command()
@click.argument('build_config', type=click.File('rb'), nargs=-1)
@click.option('--app-name', '-a', help='The app you want to build')
@click.option('--tag', '-t', help='The version tag of the app to build')
def build(build_config, app_name=None, tag=None):
    """Trigger new a build.

    The `build_config` is a YAML file with the require fields
    necessary to do the build. If no build_config is provided, your
    $EDITOR will be opened with a template that can be used to
    configure the build.
    """
    tmpl = {
        'app': str(app_name) or '',
        'tag': str(tag) or '',
        'os_image': ''
    }
    vr = get_vr()

    # grab our images and apps to validate them.
    images = query('OSImage', vr)
    apps = query('App', vr)

    # Do we use some pre-canned yaml?
    if build_config:
        config = load_yaml(build_config[0])

    # How about some command line flags
    elif app_name and tag:
        config = tmpl

    # No? We'll use our template and editor
    else:
        config = edit_yaml(dump_yaml(tmpl))

    # We have a config so we'll actually do stuff
    if config:
        config = validate(config, apps, images)
        build = models.Build(vr, config)
        build.assemble()

        click.echo('Watching for events. Hit C-c to exit')
        for event in filtered_events(vr, forever=True):
            click.echo(event)
