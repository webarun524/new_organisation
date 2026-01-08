from unittest.mock import MagicMock, patch

import pytest

from src.shared.boto import ssm


def test_get_ssm_param_success(ssm_client, assumed_session):
    param_name = "my-param"
    param_value = "my-value"
    arn = f"arn:aws:ssm:us-east-1:123456789012:parameter/{param_name}"
    ssm_client.put_parameter(Name=param_name, Value=param_value, Type="SecureString")
    # moto does not return ARN, so patch response
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()
        mock.get_parameter.return_value = {
            "Parameter": {"Value": param_value, "ARN": arn}
        }
        mock_client.return_value = mock
        result = ssm.get_ssm_param(assumed_session, param_name)
        assert result.value == param_value
        assert result.arn == arn


def test_get_ssm_param_not_found(assumed_session):
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()
        mock.get_parameter.side_effect = Exception("NotFound")
        mock_client.return_value = mock
        with pytest.raises(Exception):
            ssm.get_ssm_param(assumed_session, "does-not-exist")
