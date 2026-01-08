import logging

import boto3

from ..models.models import SecretValues

logger = logging.getLogger(__name__)


def fetch_required_secrets(session: boto3.Session, service_name: str) -> SecretValues:
    logger.info("Fetching required secrets from Secrets Manager")
    sm = session.client("secretsmanager")
    ssm_format_service_name = service_name.replace("-", "/")

    name = f"/{ssm_format_service_name}/test_admin_user_password"
    resp = sm.get_secret_value(SecretId=name)

    if "SecretString" not in resp:
        logger.exception("Secret missing in response")
        raise Exception("Secret missing")

    logger.info("Fetched Secret successfully")
    return SecretValues(
        admin_password=resp["SecretString"], admin_password_arn=resp["ARN"]
    )
