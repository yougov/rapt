"""These are helpers for working with the models / json docs from
vr.common."""
from vr.common import models


def query(name, vr, query=None):
    model = getattr(models, name, None)
    if not model:
        raise Exception('%s is not a valid vr.common.model' % name)
    doc = vr.query(model.base, query or None)
    if 'objects' in doc and doc['objects']:
        return [model(vr, obj) for obj in doc['objects']]

    print(doc)
    return []
