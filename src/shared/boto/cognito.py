import boto3


def cognito_user_exists(
    session: boto3.Session, user_pool_id: str, username: str
) -> bool:
    client = session.client("cognito-idp")
    try:
        client.admin_get_user(UserPoolId=user_pool_id, Username=username)
        return True
    except client.exceptions.UserNotFoundException:
        return False


def set_cognito_user_password(
    session: boto3.Session, user_pool_id: str, username: str, new_password: str
) -> None:
    client = session.client("cognito-idp")
    client.admin_set_user_password(
        UserPoolId=user_pool_id,
        Username=username,
        Password=new_password,
        Permanent=True,
    )
