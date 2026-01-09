class BitbucketError(Exception):
    """Base exception for Bitbucket errors"""

    pass


class PipelineTriggerError(BitbucketError):
    """Raised when pipeline trigger fails"""

    pass


class PipelineStatusError(BitbucketError):
    """Raised when pipeline status check fails"""

    pass


class PipelineFailedError(BitbucketError):
    """Raised when pipeline execution fails"""

    pass


class PipelineTimeoutError(BitbucketError):
    """Raised when pipeline execution times out"""

    pass


class ArtifactFileError(BitbucketError):
    """Raised when fetching commits file fails"""

    pass


class InvalidResponseError(BitbucketError):
    """Raised when API response is invalid or malformed"""

    pass
