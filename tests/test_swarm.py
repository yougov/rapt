from mock import patch
from collections import namedtuple

from rapt.rapt import rapt
from rapt.cmds.swarms import get_vr

FakeSwarm = namedtuple('FakeSwarm', ['name'])


class TestSwarms(object):

    def setup(self):
        self.query_patcher = patch('rapt.cmds.swarms.query')
        self.query = self.query_patcher.start()

    def teardown(self):
        self.query_patcher.stop()

    def test_swarms_output(self, cli):
        self.query.return_value = [
            FakeSwarm('foo'),
            FakeSwarm('bar')
        ]
        result = cli.invoke(rapt, ['swarms'])
        assert result.output == 'foo\nbar\n'

    def test_swarms_default_query(self, cli):
        cli.invoke(rapt, ['swarms'])

        self.query.assert_called_with('Swarm', get_vr(), {})

    def test_swarms_by_app(self, cli):
        cli.invoke(rapt, ['swarms', '-a', 'foo'])

        self.query.assert_called_with('Swarm', get_vr(), {
            'app__name__icontains': 'foo'
        })

    def test_swarms_by_config(self, cli):
        cli.invoke(rapt, ['swarms', '-c', 'foo'])

        self.query.assert_called_with('Swarm', get_vr(), {
            'config_name': 'foo'
        })

    def test_swarms_by_proc_name(self, cli):
        cli.invoke(rapt, ['swarms', '-p', 'foo'])

        self.query.assert_called_with('Swarm', get_vr(), {
            'proc_name': 'foo'
        })

    def test_swarms_by_args(self, cli):
        cli.invoke(rapt, ['swarms', '-p', 'foo', '-c', 'bar'])

        self.query.assert_called_with('Swarm', get_vr(), {
            'config_name': 'bar',
            'proc_name': 'foo'
        })
