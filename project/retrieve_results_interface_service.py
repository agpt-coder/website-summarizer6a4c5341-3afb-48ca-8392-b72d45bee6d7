from typing import List

import prisma
import prisma.models
from pydantic import BaseModel


class ContentSummaryOut(BaseModel):
    """
    Contains the details of the summarized content.
    """

    contentId: str
    summaryText: str
    originalUrl: str


class ResultsOutput(BaseModel):
    """
    Model for outputting the summarization results of a given parsing job.
    """

    jobStatus: str
    summaryResults: List[ContentSummaryOut]


async def retrieve_results_interface(taskId: str) -> ResultsOutput:
    """
    Provides an interface to access summarization results.

    Args:
    taskId (str): Unique identifier for the parsing job to retrieve results for.

    Returns:
    ResultsOutput: Model for outputting the summarization results of a given parsing job.

    Example:
        taskId = "some-task-id"
        results = await retrieve_results_interface(taskId)
        print(results)
        >>> ResultsOutput(jobStatus="Completed", summaryResults=[ContentSummaryOut(contentId="1", summaryText="This is a summary.", originalUrl="https://example.com")])
    """
    parsed_site = await prisma.models.ParsedSite.prisma().find_unique(
        where={"id": taskId}, include={"contentSummaries": True}
    )
    if not parsed_site:
        raise ValueError(f"No parsed site found with taskId: {taskId}")
    summary_results = [
        ContentSummaryOut(
            contentId=summary.id,
            summaryText=summary.summary or "",
            originalUrl=parsed_site.url,
        )
        for summary in parsed_site.contentSummaries
    ]
    result = ResultsOutput(
        jobStatus=parsed_site.status.name, summaryResults=summary_results
    )
    return result
