"""These are helpers for working with the models / json docs from
vr.common."""
from vr.common import models


def apps(vr):
    # find some info to help fill in the JSON
    doc = vr.query(models.App.base, {})
    return doc['objects']


def buildpacks(vr):
    doc = vr.query(models.Buildpack.base, {})
    return doc['objects']
