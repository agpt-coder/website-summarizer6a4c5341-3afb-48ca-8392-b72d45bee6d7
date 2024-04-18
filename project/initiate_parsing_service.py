from uuid import uuid4

import prisma
import prisma.enums
import prisma.models
from pydantic import BaseModel


class InitiateParsingResponse(BaseModel):
    """
    This model provides feedback on the initiation of the parsing process, including a unique task identifier for the job.
    """

    task_id: str
    message: str
    status: str


async def initiate_parsing(url: str) -> InitiateParsingResponse:
    """
    Starts the website parsing process for a given URL.

    Args:
    url (str): The URL of the website to be parsed.

    Returns:
    InitiateParsingResponse: This model provides feedback on the initiation of the parsing process,
    including a unique task identifier for the job.
    """
    try:
        task_id = str(uuid4())
        user_id = "user_id_extracted_from_context"
        await prisma.models.ParsedSite.prisma().create(
            data={
                "id": task_id,
                "url": url,
                "status": prisma.enums.ParsedSiteStatus.PENDING,
                "userId": user_id,
            }
        )
        return InitiateParsingResponse(
            task_id=task_id,
            message="Parsing initiation successfully started.",
            status="INITIATED",
        )
    except Exception as e:
        return InitiateParsingResponse(
            task_id="",
            message=f"Failed to initiate parsing due to error: {str(e)}",
            status="ERROR",
        )
