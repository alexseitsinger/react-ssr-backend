import pytest
from click.testing import CliRunner

from ..cli import main


def test_server_starts_and_stays_running():
    runner = CliRunner()
    result = runner.invoke(main, ["start"])
    assert result.exit_code == 0
