"""Exceptions for the tools module."""


class PathSecurityError(Exception):
    """Raised when a path attempts to escape the working directory."""

    pass
