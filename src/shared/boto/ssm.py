import boto3

from .models import SSMResponse


def get_ssm_param(session: boto3.Session, name: str) -> SSMResponse:
    client = session.client("ssm")
    resp = client.get_parameter(Name=name, WithDecryption=True)
    assert "Parameter" in resp
    assert "Value" in resp["Parameter"]
    assert "ARN" in resp["Parameter"]
    return SSMResponse(value=resp["Parameter"]["Value"], arn=resp["Parameter"]["ARN"])
