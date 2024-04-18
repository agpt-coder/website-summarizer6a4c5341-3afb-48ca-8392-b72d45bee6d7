from uuid import uuid4

import prisma
import prisma.models
from pydantic import BaseModel


class StartParsingInterfaceResponse(BaseModel):
    """
    Response model for a request to start a website parsing job. Provides feedback on the task submission status.
    """

    message: str
    taskId: str
    status: str


async def start_parsing_interface(url: str) -> StartParsingInterfaceResponse:
    """
    Provides an interface for users to submit websites for parsing.

    This function takes a URL as input, submits a new website parsing job to the database
    with an initial status of PENDING, and returns a response indicating the acceptance of the parsing job
    along with a unique taskId for tracking. It handles the creation of a new parsed site record in the database
    and prepares a response including the task ID and the initial status.

    Args:
        url (str): The URL of the website to be parsed.

    Returns:
        StartParsingInterfaceResponse: Response model for a request to start a website parsing job.
        Provides feedback on the task submission status including a unique taskId and the initial status of the parsing request.

    Example:
        response = await start_parsing_interface('https://example.com')
        >>> response.message: 'Parsing job submitted successfully.'
        >>> response.taskId: '123e4567-e89b-12d3-a456-426614174000'
        >>> response.status: 'PENDING'
    """
    task_id = str(uuid4())
    new_site = await prisma.models.ParsedSite.prisma().create(
        data={"id": task_id, "url": url, "status": "PENDING"}
    )
    return StartParsingInterfaceResponse(
        message="Parsing job submitted successfully.",
        taskId=new_site.id,
        status="PENDING",
    )
