import pytest

from vlmfw.cli import main


def test_unimplemented_command_exits_with_code_2(capsys):
    assert main(["generate"]) == 2
    assert "not implemented" in capsys.readouterr().err


def test_command_is_required():
    with pytest.raises(SystemExit):
        main([])
