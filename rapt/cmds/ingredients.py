import click

from rapt.connection import get_vr
from rapt.models import query
from rapt.util import dump_yaml, load_yaml, edit_yaml


@click.command()
@click.option('--name', '-n')
def ingredients(name):
    """List builds.
    """
    vr = get_vr()

    q = {}
    if name:
        q['name'] = name

    # add filters if we need to be...
    for i, ingredient in enumerate(query('Ingredient', vr, q)):
        click.echo(ingredient.name)


@click.command()
@click.argument('name')
@click.option('--read', '-r', is_flag=True,
              help='Read the config elements', default=False)
def ingredient(name, read):
    """View a complete ingredient config."""
    vr = get_vr()
    q = {'name': name}
    ingredient = query('Ingredient', vr, q).next()

    doc = {
        'config': load_yaml(ingredient.config_yaml),
        'env': load_yaml(ingredient.env_yaml),
    }

    if read:
        click.echo(dump_yaml(doc))
        return

    config = edit_yaml(dump_yaml(doc))

    if not config:
        click.echo('No changes')
        return

    ingredient.config_yaml = dump_yaml(config['config'])
    ingredient.env_yaml = dump_yaml(config['env'])
    ingredient.save()
