from unittest.mock import MagicMock, patch

from src.lambdas.execution_record_handler import handler


@patch.object(handler.EnvValidator, "all_env_vars_present", return_value=True)
@patch.object(handler.ExecutionRecordValidator, "validate", return_value=True)
@patch.object(
    handler.ExecutionRecordFactory,
    "make_test_execution_record",
    return_value={
        "Id": "id",
        "CreatedAt": "now",
        "UpdatedAt": "now",
        "WorkloadVersion": "v1",
    },
)
@patch.object(
    handler,
    "ExecutionRecordModel",
    side_effect=lambda **kwargs: MagicMock(
        to_dict=lambda: {"Id": "id", "WorkloadVersion": "v1"}, save=lambda: None
    ),
)
@patch.object(
    handler,
    "create_response",
    side_effect=lambda code, body: {"statusCode": code, "body": body},
)
def test_lambda_handler_success(
    mock_create_response, mock_db_model, mock_factory, mock_validator, mock_env
):
    event = {"Status": "initialized"}
    context = MagicMock()
    result = handler.lambda_handler(event, context)
    assert result["statusCode"] == 200
    assert "db_record" in result["body"]


@patch(
    "src.lambdas.execution_record_handler.handler.create_error_response",
    lambda code, msg: {"statusCode": code, "body": msg},
)
@patch.object(handler.EnvValidator, "all_env_vars_present", return_value=False)
def test_lambda_handler_missing_env(mock_env_vars_present):
    event = {"Status": "initialized"}
    context = MagicMock()
    result = handler.lambda_handler(event, context)
    assert result["statusCode"] == 500
    assert "Missing environment variables" in result["body"]


@patch(
    "src.lambdas.execution_record_handler.handler.create_error_response",
    lambda code, msg: {"statusCode": code, "body": msg},
)
@patch.object(handler.EnvValidator, "all_env_vars_present", return_value=True)
@patch.object(
    handler.ExecutionRecordValidator, "validate", side_effect=ValueError("fail")
)
def test_lambda_handler_validation_error(mock_validator, mock_env):
    event = {}
    context = MagicMock()
    result = handler.lambda_handler(event, context)
    assert result["statusCode"] == 400
    assert "fail" in result["body"]
