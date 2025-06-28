from typer.testing import CliRunner

from civic_data_boundaries_us_cd118.cli.cli import app

runner = CliRunner()


def test_fetch():
    result = runner.invoke(app, ["fetch"])
    assert result.exit_code == 0
