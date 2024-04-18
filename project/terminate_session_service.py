import prisma
import prisma.models
from pydantic import BaseModel


class TerminateSessionResponse(BaseModel):
    """
    Defines the success status upon terminating a session.
    """

    success: bool
    message: str


async def terminate_session(sessionId: str) -> TerminateSessionResponse:
    """
    Terminates an existing session based on session ID.

    This function attempts to find a session with the given ID and set its valid flag to False, effectively terminating the session.
    If the session is found and successfully updated, it returns a success message; otherwise, it returns an appropriate error message.

    Args:
        sessionId (str): The unique identifier of the session to terminate.

    Returns:
        TerminateSessionResponse: An object indicating whether the session termination was successful,
        along with a message describing the outcome.

    Example:
        session_id = "12345"
        response = await terminate_session(session_id)
        print(response.success, response.message)
        # True, "Session terminated successfully." or False, "Session not found."
    """
    try:
        session = await prisma.models.Session.prisma().find_unique(
            where={"id": sessionId}
        )
        if session is not None and session.valid:
            await prisma.models.Session.prisma().update(
                where={"id": sessionId}, data={"valid": False}
            )
            return TerminateSessionResponse(
                success=True, message="Session terminated successfully."
            )
        elif session is not None and (not session.valid):
            return TerminateSessionResponse(
                success=False, message="Session already terminated."
            )
        else:
            return TerminateSessionResponse(success=False, message="Session not found.")
    except Exception as e:
        return TerminateSessionResponse(
            success=False, message=f"An error occurred: {e}"
        )
