from unittest.mock import MagicMock, patch

import pytest

from src.lambdas.execution_params_validator import handler


@pytest.fixture
def valid_event(mock_sfn_exec_params):
    return mock_sfn_exec_params.copy()


def test_lambda_handler_success(valid_event):
    result = handler.lambda_handler(valid_event, MagicMock())
    assert result["statusCode"] == 200
    assert result["body"] == valid_event


@patch(
    "src.lambdas.execution_params_validator.models.sfn_params.SfnParams.model_validate"
)
def test_lambda_handler_validation_error(
    mock_validate, valid_event, make_validation_error
):
    mock_validate.side_effect = make_validation_error
    result = handler.lambda_handler(valid_event, MagicMock())
    assert result["statusCode"] == 400
    assert "ValidationError" in result["body"]["error"]
    assert "Invalid request parameters" in result["body"]["message"]
