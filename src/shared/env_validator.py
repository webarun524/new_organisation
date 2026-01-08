import os


class EnvValidator:
    @staticmethod
    def all_env_vars_present(env_variable_keys: list[str]) -> bool:
        return all(key in os.environ for key in env_variable_keys)
