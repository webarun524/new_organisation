from unittest.mock import MagicMock, patch

from src.lambdas.execution_record_handler.const.env_variable_keys import (
    HASH_KEY_NAME_ENV_VAR,
)
from src.lambdas.execution_record_handler.services.execution_record_factory import (
    ExecutionRecordFactory,
)


@patch.dict("os.environ", {HASH_KEY_NAME_ENV_VAR: "Id"})
@patch(
    "src.lambdas.execution_record_handler.services.execution_record_factory.ExecutionRecordModel"
)
def test_make_test_execution_record_new(mock_model):
    payload = {"foo": "bar"}
    mock_model.get.side_effect = Exception("DoesNotExist")
    record = ExecutionRecordFactory.make_test_execution_record(payload)
    assert "Id" in record
    assert "CreatedAt" in record
    assert "UpdatedAt" in record
    assert record["foo"] == "bar"
    assert isinstance(record["CreatedAt"], str)
    assert isinstance(record["UpdatedAt"], str)


@patch.dict("os.environ", {HASH_KEY_NAME_ENV_VAR: "Id"})
@patch(
    "src.lambdas.execution_record_handler.services.execution_record_factory.ExecutionRecordModel"
)
def test_make_test_execution_record_existing(mock_model):
    payload = {"Id": "exists", "foo": "baz"}
    dummy = MagicMock()
    dummy.to_dict.return_value = {
        "Id": "exists",
        "CreatedAt": "2020-01-01T00:00:00",
        "UpdatedAt": "2020-01-02T00:00:00",
    }
    mock_model.get.return_value = dummy
    record = ExecutionRecordFactory.make_test_execution_record(payload)
    assert record["Id"] == "exists"
    assert record["foo"] == "baz"
    assert isinstance(record["CreatedAt"], str)
    assert isinstance(record["UpdatedAt"], str)
