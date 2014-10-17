import os
import getpass

from urlparse import urlparse

import keyring

from vr.common.models import Velociraptor


def auth_domain(url):
    hostname = urlparse(url).hostname
    _, _, default_domain = hostname.partition('.')
    return default_domain


def set_password(url, username):
    hostname = auth_domain(url) or 'localhost'
    os.environ['VELOCIRAPTOR_AUTH_DOMAIN'] = hostname
    password = os.environ.get('VELOCIRAPTOR_PASSWORD', None)

    if password:
        keyring.set_password(hostname, username, password)

    password = keyring.get_password(hostname, username)

    if not password:
        prompt_tmpl = "{username}@{hostname}'s password: "
        prompt = prompt_tmpl.format(username=username, hostname=hostname)
        password = getpass.getpass(prompt)
        keyring.set_password(hostname, username, password)


def get_vr(username=None):
    username = os.environ['VELOCIRAPTOR_USERNAME']
    base = os.environ['VELOCIRAPTOR_URL']

    set_password(base, username)

    return Velociraptor(base=base, username=username)
