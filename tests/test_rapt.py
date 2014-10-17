"""Test for our primary entry point."""
from mock import patch

from click.testing import CliRunner

from rapt.rapt import rapt, os


class TestRapt(object):

    def setup(self):
        self.runner = CliRunner()

    @patch('rapt.rapt.os.environ', {})
    def test_username_password(self):
        self.runner.invoke(rapt, [
            '--username', 'foo', '--host', 'bar', 'info'
        ])

        env = os.environ
        assert env['VELOCIRAPTOR_URL'] == 'bar'
        assert env['VELOCIRAPTOR_USERNAME'] == 'foo'

    @patch('rapt.rapt.os.environ', {})
    def test_username_password_short(self):
        self.runner.invoke(rapt, [
            '-u', 'foo', '-H', 'bar', 'info'
        ])

        env = os.environ
        assert env['VELOCIRAPTOR_URL'] == 'bar'
        assert env['VELOCIRAPTOR_USERNAME'] == 'foo'
