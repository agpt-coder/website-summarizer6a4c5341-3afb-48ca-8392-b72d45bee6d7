from typing import Optional

import httpx
from pydantic import BaseModel, ValidationError


class SummarizeContentResponse(BaseModel):
    """
    Response model after sending web content to Claude 3 Opus for summarization. Includes the original content and its summarized version.
    """

    original_content: str
    summarized_content: str
    summary_quality: str


async def send_for_summarization(
    content: str, context: Optional[str], language: str
) -> SummarizeContentResponse:
    """
    Sends parsed content data to Claude 3 Opus for summarization.

    Args:
        content (str): The extracted web content that needs to be summarized.
        context (Optional[str]): Optional context to help improve summarization accuracy. Might include the website's URL or any relevant meta information.
        language (str): The primary language of the content. Helps in selecting the right language model for summarization.

    Returns:
        SummarizeContentResponse: Response model after sending web content to Claude 3 Opus for summarization. Includes the original content and its summarized version.

    Raises:
        ValidationError: If the response model fails to validate the summarization response.
        HTTPError: If the request to the Claude 3 Opus API fails.

    Example:
        response = send_for_summarization("This is the content to summarize.", None, "en")
        print(response)
    """
    api_endpoint = "https://claude3opus.example.com/summarize"
    headers = {"Content-Type": "application/json", "Accept-Language": language}
    payload = {"content": content, "context": context, "language": language}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_endpoint, json=payload, headers=headers)
            response.raise_for_status()
            summarize_data = response.json()
            summarize_response = SummarizeContentResponse(
                original_content=summarize_data["original_content"],
                summarized_content=summarize_data["summarized_content"],
                summary_quality=summarize_data["summary_quality"],
            )
            return summarize_response
        except ValidationError as ve:
            print("Validation error with the summarization response:", ve.json())
            raise
        except httpx.HTTPError as he:
            print("HTTP error occurred while contacting Claude 3 Opus:", str(he))
            raise
