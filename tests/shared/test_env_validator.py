from unittest.mock import patch

from shared.env_validator import EnvValidator
from src.lambdas.execution_record_handler.const.env_variable_keys import (
    ENV_VARIABLE_KEYS,
)

CORRECT_ENV_VARS = {key: "value" for key in ENV_VARIABLE_KEYS}
INCORRECT_ENV_VARS = {
    key: "value" for key in ENV_VARIABLE_KEYS if key != ENV_VARIABLE_KEYS[0]
}


@patch.dict("os.environ", CORRECT_ENV_VARS)
def test_all_env_vars_present_true():
    assert EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS) is True


@patch.dict("os.environ", INCORRECT_ENV_VARS, clear=True)
def test_all_env_vars_present_false():
    assert EnvValidator.all_env_vars_present(ENV_VARIABLE_KEYS) is False
