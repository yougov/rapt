import sys
import yaml
import click


def load_yaml(fh_or_string):
    return yaml.safe_load(fh_or_string)


def dump_yaml(obj):
    return yaml.dump(obj, default_flow_style=False)


def edit_yaml(content='', footer=''):
    MARKER = '# Everything below is ignored\n\n'
    message = click.edit(content + '\n\n' + MARKER + footer,
                         extension='.yaml')
    if message is not None:
        yaml_content = message.split(MARKER, 1)[0].rstrip('\n')
        return yaml.safe_load(yaml_content)


def stdin():
    for line in sys.stdin:
        yield line.strip()
