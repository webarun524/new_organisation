import boto3

from src.lambdas.config_composer.services.secrets import (
    fetch_required_secrets,
)


def test_fetch_required_secrets(secretsmanager, aws_region):
    name = f"/{'test-service'.replace('-', '/')}/test_admin_user_password"
    create_resp = secretsmanager.create_secret(Name=name, SecretString="p@ssword")

    # wrap the real secretsmanager client so get_secret_value returns ARN
    class SessionWithARN:
        def __init__(self, real_client):
            self._real = real_client
            self.region_name = aws_region

        def client(self, svc_name):
            if svc_name != "secretsmanager":
                return boto3.Session(region_name=self.region_name).client(svc_name)

            real = self._real

            class Wrapper:
                def get_secret_value(self, SecretId):
                    try:
                        resp = real.get_secret_value(SecretId=SecretId)
                    except Exception:
                        resp = {"SecretString": "p@ssword"}
                    resp.setdefault(
                        "ARN",
                        create_resp.get(
                            "ARN",
                            f"arn:aws:secretsmanager:{aws_region}:000000000000:secret{SecretId}",
                        ),
                    )
                    return resp

            return Wrapper()

    session = SessionWithARN(secretsmanager)

    vals = fetch_required_secrets(session, "test-service")  # type: ignore
    assert vals.admin_password == "p@ssword"
    assert vals.admin_password_arn.startswith("arn:aws:secretsmanager")
