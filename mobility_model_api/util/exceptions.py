class InvalidAccessException(Exception):
    """Raised when a requested path leaves the allowed model output root."""


class NoResultException(Exception):
    """Raised when no model result files are available for a query."""
