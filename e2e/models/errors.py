class MissingReportsDirectory(Exception):
    """Reports directory does not exist"""

    pass


class MissingReportFiles(Exception):
    """Reports directory contains no report files"""

    pass


class InvalidTestMarkValue(Exception):
    """Invalid test mark value"""

    pass


class MissingReportValue(Exception):
    """Missing required report value"""

    pass
