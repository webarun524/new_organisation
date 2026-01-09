import boto3

from .models import SecretResponse


def get_secret(session: boto3.Session, name: str) -> SecretResponse:
    client = session.client("secretsmanager")
    resp = client.get_secret_value(SecretId=name)
    return SecretResponse(value=resp["SecretString"], arn=resp["ARN"])
