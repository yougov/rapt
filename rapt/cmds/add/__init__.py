import click


from .swarm import swarm
from .app import app
from .buildpack import buildpack


@click.group()
def add():
    """Add new models."""
    pass


add.add_command(swarm)
add.add_command(app)
add.add_command(buildpack)
