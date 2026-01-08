from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class SecretValues:
    admin_password: str
    admin_password_arn: str


@dataclass
class SSMValues:
    admin_username: str
    admin_username_arn: str
    operations_portal_url: str
    operations_portal_url_arn: str
    bb_env_code: str
    bb_env_code_arn: str
    bb_env_name: str
    bb_env_name_arn: str


class ConfigComposerResult(BaseModel):
    admin_username: str
    admin_username_arn: str
    operations_portal_url: str
    operations_portal_url_arn: str
    bb_env_code: str
    bb_env_code_arn: str
    bb_env_name: str
    bb_env_name_arn: str
    admin_password_arn: str

    @classmethod
    def create_instance(
        cls,
        admin_password_arn: str,
        admin_username: str,
        admin_username_arn: str,
        operations_portal_url: str,
        operations_portal_url_arn: str,
        bb_env_code: str,
        bb_env_code_arn: str,
        bb_env_name: str,
        bb_env_name_arn: str,
    ):
        return cls(
            admin_password_arn=admin_password_arn,
            admin_username=admin_username,
            admin_username_arn=admin_username_arn,
            operations_portal_url=operations_portal_url,
            operations_portal_url_arn=operations_portal_url_arn,
            bb_env_code=bb_env_code,
            bb_env_code_arn=bb_env_code_arn,
            bb_env_name=bb_env_name,
            bb_env_name_arn=bb_env_name_arn,
        )
