import logging
import os

from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from shared.boto.cognito import cognito_user_exists, set_cognito_user_password
from shared.boto.models import SecretResponse, SSMResponse
from shared.boto.secrets import get_secret
from shared.boto.ssm import get_ssm_param
from shared.boto.sts import assume_role
from shared.env_validator import EnvValidator
from shared.utils import create_error_response, create_response

from .models.env_variables import (
    DP_COGNITO_USER_POOL_ID_PARAMETER_NAME_ENV_VAR,
    DP_PASSWORD_SECRET_NAME_ENV_VAR,
    ENV_VARIABLE_KEYS,
)
from .models.params import RequestParams

logger = logging.getLogger("config_composer")
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, _context: LambdaContext):
    logger.info(f"dp_password_rotator - Processing event: {event}")

    # Validate request parameters
    try:
        data: RequestParams = RequestParams.model_validate(event)
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

    # Assume role in data portal
    try:
        role_arn = f"arn:aws:iam::{data.dp_account_id}:role/edi-e2e-tests-cognito-secrets-ssm-cross-role"
        assumed_session = assume_role(role_arn, "E2ECognitoPasswordRotation")
        logger.info(f"Assumed role: {role_arn}")
    except Exception as e:
        logger.error(f"Failed to assume role: {e}")
        return create_error_response(500, f"Assume role error: {e}")

    # Secrets
    try:
        password_secret_name = os.environ.get(DP_PASSWORD_SECRET_NAME_ENV_VAR, "")
        password_secret: SecretResponse = get_secret(
            assumed_session, password_secret_name
        )
        logger.info(
            f"Fetched required secrets from Secrets Manager: {password_secret_name}, {password_secret.arn}"
        )
    except Exception as e:
        logger.error(f"Failed to fetch secrets: {e}")
        return create_error_response(500, f"Secrets fetch error: {e}")

    # SSM Parameters
    try:
        user_pool_id_param_name = os.environ.get(
            DP_COGNITO_USER_POOL_ID_PARAMETER_NAME_ENV_VAR, ""
        )
        user_pool_id_param: SSMResponse = get_ssm_param(
            assumed_session, user_pool_id_param_name
        )
        logger.info(
            f"Fetched SSM parameter: {user_pool_id_param_name}, {user_pool_id_param.arn}"
        )
    except Exception as e:
        logger.error(f"Failed to fetch SSM parameter: {e}")
        return create_error_response(500, f"SSM fetch error: {e}")

    # Cognito
    try:
        user_result = cognito_user_exists(
            session=assumed_session,
            user_pool_id=user_pool_id_param.value,
            username=data.e2e_user,
        )
        if not user_result:
            logger.error(
                f"Cognito user {data.e2e_user} does not exist in user pool {user_pool_id_param.value}"
            )
            return create_error_response(404, f"Cognito user {data.e2e_user} not found")
    except Exception as e:
        logger.error(f"Failed to check Cognito user existence: {e}")
        return create_error_response(500, f"Cognito user check error: {e}")

    try:
        set_cognito_user_password(
            session=assumed_session,
            user_pool_id=user_pool_id_param.value,
            username=data.e2e_user,
            new_password=password_secret.value,
        )
        logger.info(
            f"Set new password for Cognito user {data.e2e_user} in user pool {user_pool_id_param.value}"
        )
    except Exception as e:
        logger.error(f"Failed to set Cognito user password: {e}")
        return create_error_response(500, f"Cognito password set error: {e}")

    # Result
    logger.info("Password rotation successful")
    return create_response(
        200,
        {"dp_password_arn": password_secret.arn, "cross_account_role_arn": role_arn},
    )
