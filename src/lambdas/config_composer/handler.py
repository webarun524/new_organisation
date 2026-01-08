import logging
import os

import boto3
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from shared.env_validator import EnvValidator
from shared.utils import create_error_response, create_response

from .const.env_variable_keys import (
    ENV_VARIABLE_KEYS,
    SERVICE_NAME_ENV_VAR,
)
from .models.models import ConfigComposerResult
from .models.params import RequestParams
from .services.secrets import fetch_required_secrets
from .services.ssm import fetch_required_ssm_params

logger = logging.getLogger("config_composer")
logger.setLevel(logging.INFO)


SERVICE_NAME = os.environ[SERVICE_NAME_ENV_VAR]


def lambda_handler(event: dict, _context: LambdaContext):
    logger.info(f"Processing event: {event}")

    # Validate request parameters
    try:
        _data = RequestParams.model_validate(event)
    except ValidationError as e:
        logger.error(f"Request validation failed: {e}")
        error_details = "; ".join(
            [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        )
        return create_error_response(
            400, f"Invalid request parameters: {error_details}", "ValidationError"
        )

    # Validate environment variables
    if not EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS):
        return create_error_response(
            500, "env_validation: Missing environment variables"
        )
    logger.info("All required environment variables present")

    # Params + secrets
    base_session = boto3.Session()
    try:
        ssm_params = fetch_required_ssm_params(base_session, SERVICE_NAME)
        sm_secrets = fetch_required_secrets(base_session, SERVICE_NAME)
        logger.info(f"Fetched SSM params and secrets: {ssm_params}")
    except Exception as e:
        logger.exception("Failed to fetch params/secrets")
        return create_error_response(500, f"fetch_params_secrets_error: {e}")

    # Compose config
    config = ConfigComposerResult.create_instance(
        admin_password_arn=sm_secrets.admin_password_arn,
        admin_username=ssm_params.admin_username,
        admin_username_arn=ssm_params.admin_username_arn,
        operations_portal_url=ssm_params.operations_portal_url,
        operations_portal_url_arn=ssm_params.operations_portal_url_arn,
        bb_env_code=ssm_params.bb_env_code,
        bb_env_code_arn=ssm_params.bb_env_code_arn,
        bb_env_name=ssm_params.bb_env_name,
        bb_env_name_arn=ssm_params.bb_env_name_arn,
    )

    return create_response(200, config.model_dump())
