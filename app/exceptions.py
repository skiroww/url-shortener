from fastapi import HTTPException, status

class LinkNotFoundError(HTTPException):
    def __init__(self, detail: str = "Link not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class LinkExpiredError(HTTPException):
    def __init__(self, detail: str = "Link has expired"):
        super().__init__(
            status_code=status.HTTP_410_GONE,
            detail=detail
        )

class CustomAliasTakenError(HTTPException):
    def __init__(self, detail: str = "Custom alias is already taken"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class UnauthorizedError(HTTPException):
    def __init__(self, detail: str = "Not authorized to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class InvalidCredentialsError(HTTPException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class UserExistsError(HTTPException):
    def __init__(self, detail: str = "User already exists"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class InvalidURLError(HTTPException):
    def __init__(self, detail: str = "Invalid URL"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class UnsafeURLError(HTTPException):
    def __init__(self, detail: str = "URL is not safe"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )

class InvalidAliasError(HTTPException):
    def __init__(self, detail: str = "Invalid alias format"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        ) 