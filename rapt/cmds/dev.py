import os
import sys
import subprocess

from datetime import datetime

import yaml
import click

PROVISION_SH = os.environ.get('PROVISION_SH_URL')
IMAGE_DEF = {
    'base_image_url': 'http://cdn.yougov.com/build/ubuntu_trusty_pamfix.tar.gz',
    'base_image_name': 'ubuntu_trusty_pamfix',
    'new_image_name': '',
    'script_url': '',
    'env': {
        'PATH': '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    }
}


def image_yaml(script=None, name=None):
    name = name or 'my-image-name-%s' % datetime.now().strftime('%Y-%m-%d')
    config = IMAGE_DEF.copy()
    config['new_image_name'] = name
    config['script_url'] = script or PROVISION_SH
    return config


@click.group()
def dev():
    pass


@dev.command(help='''Build a container for local development.

Take vr.imager and create a container based on the current
yg-app-base-image development locally.

IMPORTANT! This requires a Linux host!
''')
@click.option('--provision-script', '-p', default=PROVISION_SH)
@click.option('--image-name', '-n')
def build_container(provision_script, image_name=None):
    click.echo('Installing vr.imager')
    subprocess.call('pip install vr.imager'.split())

    click.echo('Generating the config')
    config = image_yaml(provision_script, image_name)
    image_filename = config['new_image_name'] + '.yaml'

    click.echo('Writing image config: %s' % image_filename)
    yaml.safe_dump(config, open(image_filename, 'w+'))

    vimage = os.path.join(sys.exec_prefix, 'bin', 'vimage')
    cmd = ['sudo', vimage, 'build', os.path.abspath(image_filename)]
    click.echo('Creating container: %s' % ' '.join(cmd))
    subprocess.call(cmd)
