from dataclasses import dataclass


@dataclass(frozen=True)
class DpTestConfig:
    url: str
    user: str
    password: str
