from dataclasses import asdict, dataclass
from typing import Optional


@dataclass(frozen=True)
class OpTestConfig:
    url: str
    user: str
    password: str
    dp_deployment_role_name: Optional[str]
    dp_account_id: Optional[str]
    dp_domain: Optional[str]
    dp_hosted_zone_id: Optional[str]
    osdu_version: Optional[str]
    enterprise_active: Optional[bool]
    dry_run_active: Optional[bool]
    region: Optional[str]
    deployment_id: Optional[str]
    teardown_trigger_active: Optional[bool]

    def __repr__(self):
        data = asdict(self)
        data["password"] = "***"
        return f"{self.__class__.__name__}({data})"
