from pydantic import BaseModel

class Token(BaseModel):
    """
    Represents an authentication token object

    Attributes:
        access_token: The actual token string used for authentication
        token_type: The type of the token, typically "Bearer" for OAuth tokens
    """

    access_token: str
    token_type: str
