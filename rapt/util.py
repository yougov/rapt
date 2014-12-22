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


def is_resource_uri(string):
    # names can't have slashes
    return '/' in string


def stringify_dict(var):
    result = {}
    for k, v in var.iteritems():
        if isinstance(v, basestring):
            v = str(v)
        elif isinstance(v, dict):
            v = stringify_dict(v)
        elif isinstance(v, list):
            v = map(str, v)

        result[str(k)] = v

    return result
