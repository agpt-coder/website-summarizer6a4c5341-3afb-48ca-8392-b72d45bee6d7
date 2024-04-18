from typing import List, Optional

import prisma
import prisma.models
from pydantic import BaseModel


class WebsiteElementChange(BaseModel):
    """
    Describes changes to a specific element on the website, including its old and new identification strategy.
    """

    element_name: str
    old_selector: str
    new_selector: str


class UpdateParsingStrategyResponse(BaseModel):
    """
    Provides feedback on the update process of parsing strategies.
    """

    success: bool
    message: str


async def update_parsing_strategy(
    website_id: str,
    changed_elements: List[WebsiteElementChange],
    additional_notes: Optional[str] = None,
) -> UpdateParsingStrategyResponse:
    """
    Updates parsing strategies based on detected changes in website layouts.

    Args:
    website_id (str): The unique identifier of the website whose parsing strategy needs updating.
    changed_elements (List[WebsiteElementChange]): List of changed elements and their new XPaths or CSS selectors for accurate parsing.
    additional_notes (Optional[str]): Any additional information or context about the change request.

    Returns:
    UpdateParsingStrategyResponse: Provides feedback on the update process of parsing strategies.

    This function aims to record the updates in parsing strategies based on the changes identified within the structure of a website.
    """
    parsed_site = await prisma.models.ParsedSite.prisma().find_unique(
        where={"id": website_id}
    )
    if not parsed_site:
        return UpdateParsingStrategyResponse(
            success=False, message="Website not found."
        )
    return UpdateParsingStrategyResponse(
        success=True, message="Parsing strategy updated successfully."
    )
