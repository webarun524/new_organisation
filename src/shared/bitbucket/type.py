from enum import Enum


class BitbucketPipelineStatus(str, Enum):
    """Pipeline execution status constants"""

    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    PENDING = "PENDING"
    PARSING = "PARSING"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def _missing_(cls, value):
        return cls.UNKNOWN
