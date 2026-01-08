import logging
from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import ValidationError

from shared.utils import create_error_response, create_response

from .models.sfn_params import SfnParams

logger = logging.getLogger("execution_params_validator")
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, _context: LambdaContext) -> dict[str, Any]:
    logger.info("Received event: %s", event)
    # validate env
    try:
        SfnParams.model_validate(event)
    except ValidationError as e:
        logger.error("Validation failed: %s", e)
        error_details = "; ".join(
            [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
        )
        return create_error_response(
            400, f"Invalid request parameters: {error_details}", "ValidationError"
        )

    # generate response
    logger.info("Returning response: %s", event)
    return create_response(200, event)
