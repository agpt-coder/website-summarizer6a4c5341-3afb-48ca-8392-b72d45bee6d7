from typing import Any, Dict, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class ParsingStatusResponse(BaseModel):
    """
    Provides the current status of the parsing task along with any relevant details.
    """

    status: str
    message: Optional[str] = None
    parsedContent: Optional[Dict[str, Any]] = None


async def check_parsing_status(taskId: str) -> ParsingStatusResponse:
    """
    Checks the status of the parsing process for a given task ID.

    Args:
        taskId (str): The unique identifier for the parsing task whose status is being queried.

    Returns:
        ParsingStatusResponse: Provides the current status of the parsing task along with any relevant details.

    Example:
        task_status = check_parsing_status("some-unique-task-id")
        print(task_status)
        > ParsingStatusResponse(status="completed", message="The parsing process completed successfully.", parsedContent={...})
    """
    parsed_site = await prisma.models.ParsedSite.prisma().find_unique(
        where={"id": taskId}, include={"contentSummaries": True}
    )
    if parsed_site:
        return ParsingStatusResponse(
            status=parsed_site.status,
            message=f"Task with ID {taskId} is {parsed_site.status}.",
            parsedContent={
                "summaries": [cs.summary for cs in parsed_site.contentSummaries]
                if parsed_site.contentSummaries
                else None
            },
        )
    else:
        return ParsingStatusResponse(
            status="error", message=f"No task found with ID {taskId}."
        )
