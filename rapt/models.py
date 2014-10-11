"""These are helpers for working with the models / json docs from
vr.common."""
import sys
import click

from vr.common import models
from requests.exceptions import ConnectionError

from .codes import CONNECTION_ERROR


def query(name, vr, query=None):
    model = getattr(models, name, None)
    if not model:
        raise Exception('%s is not a valid vr.common.model' % name)

    try:
        cursor = vr.query(model.base, query or None)
    except ConnectionError:
        click.echo('Hmm... I had some trouble connecting to Velociraptor.')
        click.echo("I'm using '%s' for the URL with the username '%s'." % (
            vr.base, vr.username
        ))
        click.echo('Does that look right?')
        sys.exit(CONNECTION_ERROR)

    for obj in cursor:
        yield model(vr, obj)
