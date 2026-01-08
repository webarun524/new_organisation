import os
from unittest.mock import MagicMock, patch

os.environ.setdefault("SERVICE_NAME", "test-service")

from src.lambdas.config_composer.handler import lambda_handler


def _call_handler_with_patches(patches, event=None):
    if event is None:
        event = {"environment": "dev"}
    mock_context = MagicMock()
    if patches:
        with patch.multiple("src.lambdas.config_composer.handler", **patches):
            return lambda_handler(event, mock_context)
    else:
        return lambda_handler(event, mock_context)


def test_lambda_handler_happy_path():
    patches = {
        "EnvValidator": MagicMock(all_env_vars_present=MagicMock(return_value=True)),
        "fetch_required_ssm_params": MagicMock(
            return_value=MagicMock(
                admin_username="admin@example.com",
                admin_username_arn="arn:aws:ssm:1",
                operations_portal_url="https://ops",
                operations_portal_url_arn="arn:aws:ssm:2",
                bb_env_code="vdev",
                bb_env_code_arn="arn:aws:ssm:3",
                bb_env_name="Dev",
                bb_env_name_arn="arn:aws:ssm:4",
            )
        ),
        "fetch_required_secrets": MagicMock(
            return_value=MagicMock(
                admin_password="p@ss", admin_password_arn="arn:aws:secretsmanager:1"
            )
        ),
    }

    resp = _call_handler_with_patches(patches)

    assert resp["statusCode"] == 200
    body = resp["body"]
    # ConfigComposerResult now returns admin_password_arn and admin_username_arn
    assert "admin_password_arn" in body and "admin_username_arn" in body


def test_env_validation_error():
    resp = _call_handler_with_patches(
        {"EnvValidator": MagicMock(all_env_vars_present=MagicMock(return_value=False))}
    )
    assert resp["statusCode"] == 500
    assert "env_validation" in resp["body"]["message"]


def test_fetch_params_secrets_error():
    patches = {
        "EnvValidator": MagicMock(all_env_vars_present=MagicMock(return_value=True)),
        "fetch_required_ssm_params": MagicMock(side_effect=Exception("ssm fail")),
        "fetch_required_secrets": MagicMock(return_value=MagicMock(admin_password="p")),
    }
    resp = _call_handler_with_patches(patches)
    assert resp["statusCode"] == 500
    assert "fetch_params_secrets_error" in resp["body"]["message"]


def test_request_validation_error():
    # Pass an invalid event (missing required 'environment') and expect 400
    patches = {}
    resp = _call_handler_with_patches(patches, event={"wrong": "value"})
    assert resp["statusCode"] == 400
    assert "Invalid request parameters" in resp["body"]["message"]
