import prisma
import prisma.models
from fastapi import HTTPException
from pydantic import BaseModel


class SummaryResponse(BaseModel):
    """
    Response model containing the retrieved summary.
    """

    summary: str
    status: str
    createdAt: str
    updatedAt: str


async def retrieve_summary(taskId: str) -> SummaryResponse:
    """
    Retrieves summarized content for a given task ID.

    This function queries the ContentSummary table using the provided task ID to find a corresponding
    summary. It constructs and returns a SummaryResponse object if the task ID exists, otherwise,
    raises an HTTPException indicating the task ID was not found.

    Args:
        taskId (str): Unique identifier for the task whose summary is being requested.

    Returns:
        SummaryResponse: Response model containing the retrieved summary.

    Raises:
        HTTPException: If no summary is found for the given task ID, raise 404 error.
    """
    content_summary = await prisma.models.ContentSummary.prisma().find_unique(
        where={"id": taskId}
    )
    if not content_summary:
        raise HTTPException(status_code=404, detail="Task ID not found")
    parsed_site = await prisma.models.ParsedSite.prisma().find_unique(
        where={"id": content_summary.parsedSiteId}
    )
    if not parsed_site:
        raise HTTPException(
            status_code=404,
            detail="Parsed site not found for the given content summary",
        )
    return SummaryResponse(
        summary=content_summary.summary
        if content_summary.summary
        else "No summary available",
        status=parsed_site.status,
        createdAt=content_summary.createdAt.isoformat(),
        updatedAt=parsed_site.updatedAt.isoformat(),
    )
