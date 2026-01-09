import logging
from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext

from shared.env_validator import EnvValidator
from shared.utils import create_error_response, create_response

from .const.env_variable_keys import ENV_VARIABLE_KEYS
from .models.execution_record import ExecutionRecordModel
from .services.execution_record_factory import ExecutionRecordFactory
from .services.execution_record_validator import ExecutionRecordValidator

logger = logging.getLogger("execution_record_handler")
logger.setLevel(logging.INFO)


def lambda_handler(event: dict, _context: LambdaContext) -> dict[str, Any]:
    logger.info("Received event: %s", event)
    # validate env
    if not EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS):
        logger.error("Missing environment variables: %s", ENV_VARIABLE_KEYS)
        return create_error_response(500, "Missing environment variables")

    # validate payload
    try:
        ExecutionRecordValidator.validate(event)
    except ValueError as e:
        logger.error("Payload validation failed: %s", e)
        return create_error_response(400, str(e))

    # build DB record
    record_dict = ExecutionRecordFactory.make_test_execution_record(event)
    logger.info("Built DB record: %s", record_dict)

    # propagate to DB
    db_record = ExecutionRecordModel(**record_dict)
    db_record.save()
    logger.info("Saved DB record to DynamoDB: %s", db_record.to_dict())

    # generate response
    response_body = {
        "message": "Record saved successfully",
        "db_record": db_record.to_dict(),
    }
    logger.info("Returning response: %s", response_body)
    return create_response(200, response_body)
