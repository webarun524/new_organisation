from pydantic import ValidationError

from shared.domain.validators.execution_record import ExecutionRecord
from shared.env_validator import EnvValidator

from ..models.const import (
    ENV_VARIABLE_KEYS,
)
from ..models.errors import (
    EnvironmentValidationError,
    ExecutionRecordMalformed,
    ParamsValidationError,
)
from ..models.params import ParamsModel


class Validator:
    @staticmethod
    def validate_environment():
        """
        Validate environment variables
        """
        if not EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS):
            error_msg = "Missing required environmental variables"
            raise EnvironmentValidationError(error_msg)

    @staticmethod
    def validate_parameters(event: dict) -> ParamsModel:
        """
        Validate request parameters
        """
        try:
            return ParamsModel.model_validate(event)
        except ValidationError as e:
            error_details = "; ".join(
                [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            )
            raise ParamsValidationError(error_details)

    @staticmethod
    def _validate_execution_record(record: dict) -> dict:
        """
        Validate response and returned record structure
        """
        try:
            ExecutionRecord.model_validate(record)
        except ValidationError as e:
            error_details = "; ".join(
                [f"{err['loc'][0]}: {err['msg']}" for err in e.errors()]
            )
            raise ExecutionRecordMalformed(error_details)

        return record
