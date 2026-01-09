import os

from aws_lambda_powertools import Logger

BITBUCKET_TOKEN_ENV_VAR = "BITBUCKET_TOKEN"

logger = Logger(service="extract-env-variables")


def get_token_from_envs() -> str:
    """Get and validate Bitbucket token from environment variables"""
    try:
        token = os.environ[BITBUCKET_TOKEN_ENV_VAR]
    except KeyError:
        logger.error(f"{BITBUCKET_TOKEN_ENV_VAR} environment variable is not set")
        raise ValueError(
            f"Missing required environment variable: {BITBUCKET_TOKEN_ENV_VAR}"
        )

    if not token or not token.strip():
        logger.error(f"{BITBUCKET_TOKEN_ENV_VAR} environment variable is empty")
        raise ValueError(f"{BITBUCKET_TOKEN_ENV_VAR} cannot be empty")

    return token.strip()
