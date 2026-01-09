import logging

import boto3
from botocore.exceptions import ClientError
from mypy_boto3_ssm import SSMClient

from ..models.models import SSMValues

logger = logging.getLogger(__name__)


def fetch_required_ssm_params(session: boto3.Session, service_name: str) -> SSMValues:
    logger.info("Fetching required SSM parameters")

    ssm: SSMClient = session.client("ssm")

    ssm_format_service_name = service_name.replace("-", "/")
    test_admin_user_name_parameter = f"/{ssm_format_service_name}/test_admin_user_name"
    operations_portal_url_parameter = (
        f"/{ssm_format_service_name}/operations_portal_url"
    )
    bb_env_code_parameter = f"/{ssm_format_service_name}/bb_env_code"
    bb_env_name_parameter = f"/{ssm_format_service_name}/bb_env_name"
    names = [
        test_admin_user_name_parameter,
        operations_portal_url_parameter,
        bb_env_code_parameter,
        bb_env_name_parameter,
    ]

    try:
        resp = ssm.get_parameters(Names=names, WithDecryption=False)
    except ClientError as e:
        logger.exception("Failed retrieving SSM params")
        raise Exception(f"Failed retrieving SSM params: {e}")

    values = {}
    arns = {}
    for p in resp["Parameters"]:
        assert "Name" in p
        assert "Value" in p
        assert "ARN" in p, f"ARN missing from SSM parameter {p['Name']}"
        name = p["Name"]
        value = p["Value"]
        arn = p["ARN"]
        values[name] = value
        arns[name] = arn

    missing = [n for n in names if n not in values]
    if missing:
        logger.exception(f"Missing SSM params: {missing}")
        raise Exception(f"Missing SSM params: {missing}")

    logger.info("Fetched all required SSM parameters")

    return SSMValues(
        admin_username=values[test_admin_user_name_parameter],
        admin_username_arn=arns[test_admin_user_name_parameter],
        operations_portal_url=values[operations_portal_url_parameter],
        operations_portal_url_arn=arns[operations_portal_url_parameter],
        bb_env_code=values[bb_env_code_parameter],
        bb_env_code_arn=arns[bb_env_code_parameter],
        bb_env_name=values[bb_env_name_parameter],
        bb_env_name_arn=arns[bb_env_name_parameter],
    )
