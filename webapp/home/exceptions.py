class ezEMLError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message):
        self.message = message


class AuthTokenExpired(ezEMLError):
    pass


class DataTableError(ezEMLError):
    pass


class InvalidXMLError(ezEMLError):
    pass


class MissingFileError(ezEMLError):
    pass


class Unauthorized(ezEMLError):
    pass


class UnknownDistributionUrl(ezEMLError):
    pass


class UnicodeDecodeErrorInternal(ezEMLError):
    pass

