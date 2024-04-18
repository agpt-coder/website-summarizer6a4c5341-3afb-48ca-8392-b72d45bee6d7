from typing import Optional

import prisma
import prisma.models
from pydantic import BaseModel


class CreateSessionResponse(BaseModel):
    """
    Response model for session creation, detailing the success status and session token.
    """

    success: bool
    session_token: Optional[str] = None
    message: str


async def create_session(
    username: str, password: str, website_url: str
) -> CreateSessionResponse:
    """
    Initiates a new session for a website that requires authentication.

    Args:
        username (str): The username of the user trying to initiate a session.
        password (str): The password for the user in plain text. This will be securely processed and never stored or logged.
        website_url (str): The URL of the website for which the session is being created.

    Returns:
        CreateSessionResponse: Response model for session creation, detailing the success status and session token.
    """
    user = await prisma.models.User.prisma().find_unique(where={"email": username})
    if user is None:
        return CreateSessionResponse(success=False, message="User not found.")
    if not verify_password(password, user.password):
        return CreateSessionResponse(success=False, message="Incorrect password.")
    session = await prisma.models.Session.prisma().create(data={"userId": user.id})
    return CreateSessionResponse(
        success=True, session_token=session.id, message="Session created successfully."
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies if a plain text password matches the hashed password.

    This is a stub function and needs proper implementation using a password hashing library.

    Args:
        plain_password (str): The plain text password input by the user.
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return True
