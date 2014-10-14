import pytest

from mock import Mock, MagicMock

from vr.common.models import App

from rapt.models import query


class TestQuery(object):
    """The query function wraps our vr.query method. The query method
    is the priamry way we talk to the VR tastypie API."""

    def test_query_valid_models(self):
        result = query('NotARealModel', Mock())

        # NOTE: We have to actually consume the result in order to get an
        #       error.
        assert pytest.raises(Exception, result.next)

    def test_query_returns_iterable(self):
        vr = MagicMock()
        result = query('App', vr)
        assert hasattr(result, 'next')

    def test_query_returns_objects(self):
        vr = MagicMock()
        vr.query.return_value = [{'name': 'foo'}]
        obj = query('App', vr).next()

        assert isinstance(obj, App)
        assert obj.name == 'foo'
