class ExecutionRecordMalformed(Exception):
    """Raised when Execution Record is malformed"""

    pass


class EnvironmentValidationError(Exception):
    """Raised when environmental variables are missing"""

    pass


class ParamsValidationError(Exception):
    """Raised when params variables are missing"""

    pass
