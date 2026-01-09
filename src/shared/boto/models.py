from dataclasses import dataclass


@dataclass
class SecretResponse:
    value: str
    arn: str


@dataclass
class SSMResponse:
    value: str
    arn: str
