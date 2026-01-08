from unittest.mock import MagicMock, patch

from src.shared.boto import cognito


def test_cognito_user_exists_true(cognito_client, assumed_session):
    user_pool_id = "us-east-1_123456789"
    username = "testuser"
    # Patch the client to simulate user exists
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()
        mock.admin_get_user.return_value = {"Username": username}
        mock_client.return_value = mock
        assert (
            cognito.cognito_user_exists(assumed_session, user_pool_id, username) is True
        )


def test_cognito_user_exists_false(assumed_session):
    user_pool_id = "us-east-1_123456789"
    username = "nouser"
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()

        class UserNotFound(Exception):
            pass

        mock.exceptions = MagicMock()
        mock.exceptions.UserNotFoundException = UserNotFound
        mock.admin_get_user.side_effect = UserNotFound()
        mock_client.return_value = mock
        assert (
            cognito.cognito_user_exists(assumed_session, user_pool_id, username)
            is False
        )


def test_set_cognito_user_password(assumed_session):
    user_pool_id = "us-east-1_123456789"
    username = "testuser"
    new_password = "Password123!"
    with patch("boto3.Session.client") as mock_client:
        mock = MagicMock()
        mock.admin_set_user_password.return_value = {}
        mock_client.return_value = mock
        cognito.set_cognito_user_password(
            assumed_session, user_pool_id, username, new_password
        )
        mock.admin_set_user_password.assert_called_once_with(
            UserPoolId=user_pool_id,
            Username=username,
            Password=new_password,
            Permanent=True,
        )
