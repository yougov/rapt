import click


from .swarm import swarm
from .app import app
from .buildpack import buildpack


@click.group()
def add():
    pass


add.add_command(swarm)
add.add_command(app)
add.add_command(buildpack)
