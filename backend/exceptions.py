class NotFoundException(Exception):
    """Exception raised when a resource is not found."""
    def __init__(self, message="Resource not found"):
        super().__init__(message)

class InvalidSolutionException(Exception):
    """Exception raised when a solution is invalid."""
    def __init__(self, message="Invalid solution"):
        super().__init__(message)
