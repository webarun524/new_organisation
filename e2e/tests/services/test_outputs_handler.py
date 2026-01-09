import json
from unittest.mock import patch

import pytest

from e2e.services.outputs_handler import OutputsHandler


# Patch OUTPUTS_FILE in both the constants and outputs_handler module for all tests
@pytest.fixture(autouse=True)
def patch_outputs_file(tmp_path, monkeypatch):
    test_file = tmp_path / "outputs.json"
    monkeypatch.setattr("e2e.tests.operations_portal.variables.OUTPUTS_FILE", test_file)
    import e2e.services.outputs_handler as outputs_handler_mod

    outputs_handler_mod.OUTPUTS_FILE = test_file
    yield test_file


@pytest.mark.operations_portal
def test_initialize_outputs_file_creates_file(patch_outputs_file):
    OutputsHandler.initialize_outputs_file()
    assert patch_outputs_file.exists()
    with open(patch_outputs_file) as f:
        data = json.load(f)
        assert data == {}


@pytest.mark.operations_portal
def test_initialize_outputs_file_skips_if_exists(patch_outputs_file, capsys):
    patch_outputs_file.write_text(json.dumps({"foo": "bar"}))
    OutputsHandler.initialize_outputs_file()
    captured = capsys.readouterr()
    assert "already exists" in captured.out
    # File should not be overwritten
    with open(patch_outputs_file) as f:
        data = json.load(f)
        assert data == {"foo": "bar"}


@pytest.mark.operations_portal
def test_save_outputs_creates_and_overwrites(patch_outputs_file):
    result = OutputsHandler.save_outputs("key1", {"a": 1})
    assert result == {"key1": {"a": 1}}
    # Overwrite with new data
    result2 = OutputsHandler.save_outputs("key1", [1, 2, 3])
    assert result2 == {"key1": [1, 2, 3]}


@pytest.mark.operations_portal
def test_save_outputs_merges_with_existing(patch_outputs_file):
    OutputsHandler.save_outputs("foo", 123)
    OutputsHandler.save_outputs("bar", 456)
    with open(patch_outputs_file) as f:
        data = json.load(f)
        assert data == {"foo": 123, "bar": 456}


@pytest.mark.operations_portal
def test_save_outputs_handles_invalid_json(patch_outputs_file):
    patch_outputs_file.write_text("not a json")
    OutputsHandler.save_outputs("x", 1)
    with open(patch_outputs_file) as f:
        data = json.load(f)
        assert data == {"x": 1}


@pytest.mark.operations_portal
def test_save_outputs_wraps_list(patch_outputs_file):
    patch_outputs_file.write_text(json.dumps([1, 2, 3]))
    OutputsHandler.save_outputs("foo", "bar")
    with open(patch_outputs_file) as f:
        data = json.load(f)
        assert data == {"foo": "bar"}


@pytest.mark.operations_portal
def test_get_outputs_success(patch_outputs_file):
    OutputsHandler.save_outputs("mykey", {"v": 42})
    out = OutputsHandler.get_outputs("mykey")
    assert out == {"v": 42}


@pytest.mark.operations_portal
def test_get_outputs_file_not_found(tmp_path):
    test_file = tmp_path / "missing.json"
    with patch("e2e.tests.operations_portal.variables.OUTPUTS_FILE", test_file):
        with pytest.raises(FileNotFoundError):
            OutputsHandler.get_outputs("foo")


@pytest.mark.operations_portal
def test_get_outputs_key_not_found(patch_outputs_file):
    OutputsHandler.save_outputs("foo", 1)
    with pytest.raises(KeyError):
        OutputsHandler.get_outputs("bar")
