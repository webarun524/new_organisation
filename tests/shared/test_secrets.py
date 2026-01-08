from unittest.mock import MagicMock, patch

import pytest

from src.shared.boto import secrets


def test_get_secret_success(secretsmanager, assumed_session):
    secret_name = "my-secret"
    secret_value = "supersecret"
    arn = "arn:aws:secretsmanager:us-east-1:123456789012:secret:my-secret"
    secretsmanager.create_secret(Name=secret_name, SecretString=secret_value)
    # boto3 moto returns a different ARN, so fetch it
    resp = secretsmanager.get_secret_value(SecretId=secret_name)
    arn = resp["ARN"]
    result = secrets.get_secret(assumed_session, secret_name)
    assert result.value == secret_value
    assert result.arn == arn


def test_get_secret_not_found(assumed_session):
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()
        mock.get_secret_value.side_effect = Exception("NotFound")
        mock_client.return_value = mock
        with pytest.raises(Exception):
            secrets.get_secret(assumed_session, "does-not-exist")
