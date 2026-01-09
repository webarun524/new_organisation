from unittest.mock import MagicMock, patch

import pytest

from src.lambdas.dp_password_rotator import handler


@pytest.fixture
def valid_event():
    return {"dp_account_id": "123456789012", "e2e_user": "testuser"}


@pytest.fixture
def valid_context():
    return MagicMock()


@patch("src.lambdas.dp_password_rotator.handler.RequestParams.model_validate")
def test_error_request_validation(
    mock_validate, valid_event, valid_context, make_validation_error
):
    mock_validate.side_effect = make_validation_error
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 400
    assert "Invalid request parameters" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=False,
)
def test_error_env_vars(mock_env, mock_validate, valid_event, valid_context):
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "env_validation" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(dp_account_id="123456789012", e2e_user="testuser"),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role")
def test_error_assume_role(
    mock_assume, mock_env, mock_validate, valid_event, valid_context
):
    mock_assume.side_effect = Exception("assume error")
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "Assume role error" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch("src.lambdas.dp_password_rotator.handler.get_secret")
def test_error_get_secret(
    mock_secret, mock_assume, mock_env, mock_validate, valid_event, valid_context
):
    mock_secret.side_effect = Exception("secret error")
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "Secrets fetch error" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch("src.lambdas.dp_password_rotator.handler.get_secret", return_value=MagicMock())
@patch("src.lambdas.dp_password_rotator.handler.get_ssm_param")
def test_error_get_ssm_param(
    mock_ssm,
    mock_secret,
    mock_assume,
    mock_env,
    mock_validate,
    valid_event,
    valid_context,
):
    mock_ssm.side_effect = Exception("ssm error")
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "SSM fetch error" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch("src.lambdas.dp_password_rotator.handler.get_secret", return_value=MagicMock())
@patch(
    "src.lambdas.dp_password_rotator.handler.get_ssm_param",
    return_value=MagicMock(value="pool", arn="arn"),
)
@patch("src.lambdas.dp_password_rotator.handler.cognito_user_exists")
def test_error_cognito_user_not_found(
    mock_exists,
    mock_ssm,
    mock_secret,
    mock_assume,
    mock_env,
    mock_validate,
    valid_event,
    valid_context,
):
    mock_exists.return_value = False
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 404
    assert "not found" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch("src.lambdas.dp_password_rotator.handler.get_secret", return_value=MagicMock())
@patch(
    "src.lambdas.dp_password_rotator.handler.get_ssm_param",
    return_value=MagicMock(value="pool", arn="arn"),
)
@patch("src.lambdas.dp_password_rotator.handler.cognito_user_exists")
def test_error_cognito_user_check(
    mock_exists,
    mock_ssm,
    mock_secret,
    mock_assume,
    mock_env,
    mock_validate,
    valid_event,
    valid_context,
):
    mock_exists.side_effect = Exception("cognito check error")
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "Cognito user check error" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch(
    "src.lambdas.dp_password_rotator.handler.get_secret",
    return_value=MagicMock(value="pw", arn="arn"),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.get_ssm_param",
    return_value=MagicMock(value="pool", arn="arn"),
)
@patch("src.lambdas.dp_password_rotator.handler.cognito_user_exists", return_value=True)
@patch("src.lambdas.dp_password_rotator.handler.set_cognito_user_password")
def test_error_set_cognito_user_password(
    mock_set_pw,
    mock_exists,
    mock_ssm,
    mock_secret,
    mock_assume,
    mock_env,
    mock_validate,
    valid_event,
    valid_context,
):
    mock_set_pw.side_effect = Exception("set pw error")
    result = handler.lambda_handler(valid_event, valid_context)
    assert result["statusCode"] == 500
    assert "Cognito password set error" in result["body"]["message"]


@patch(
    "src.lambdas.dp_password_rotator.handler.RequestParams.model_validate",
    return_value=MagicMock(dp_account_id="123456789012", e2e_user="testuser"),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.EnvValidator.all_env_vars_present",
    return_value=True,
)
@patch("src.lambdas.dp_password_rotator.handler.assume_role", return_value=MagicMock())
@patch(
    "src.lambdas.dp_password_rotator.handler.get_secret",
    return_value=MagicMock(value="pw", arn="arn"),
)
@patch(
    "src.lambdas.dp_password_rotator.handler.get_ssm_param",
    return_value=MagicMock(value="pool", arn="arn"),
)
@patch("src.lambdas.dp_password_rotator.handler.cognito_user_exists", return_value=True)
@patch(
    "src.lambdas.dp_password_rotator.handler.set_cognito_user_password",
    return_value=None,
)
def test_success(
    mock_set_pw,
    mock_exists,
    mock_ssm,
    mock_secret,
    mock_assume,
    mock_env,
    mock_validate,
    valid_event,
    valid_context,
):
    result = handler.lambda_handler(valid_event, valid_context)
    role_arn = f"arn:aws:iam::{valid_event['dp_account_id']}:role/edi-e2e-tests-cognito-secrets-ssm-cross-role"
    assert result["statusCode"] == 200
    assert result["body"]["cross_account_role_arn"] == role_arn
    assert result["body"]["dp_password_arn"] == "arn"
