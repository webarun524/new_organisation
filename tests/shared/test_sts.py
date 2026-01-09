from unittest.mock import MagicMock, patch

import boto3

from src.shared.boto import sts


def test_assume_role_success():
    fake_creds = {
        "Credentials": {
            "AccessKeyId": "AKIA...",
            "SecretAccessKey": "secret",
            "SessionToken": "token",
        }
    }
    with patch("boto3.client") as mock_client:
        mock = MagicMock()
        mock.assume_role.return_value = fake_creds
        mock_client.return_value = mock
        session = sts.assume_role("arn:aws:iam::123456789012:role/test", "mysession")
        assert isinstance(session, boto3.Session)
        # Check that credentials are set
        assert session.get_credentials() is not None
