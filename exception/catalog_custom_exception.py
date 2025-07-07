class ValidationError(Exception):
    """Raised when input validation fails."""
    pass

class CatalogNotFoundError(Exception):
    """Raised when a catalog with a specific ID is not found."""
    pass
