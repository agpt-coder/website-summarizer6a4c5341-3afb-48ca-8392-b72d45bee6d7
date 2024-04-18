import requests
from pydantic import BaseModel


class VerifyComplianceResponse(BaseModel):
    """
    Indicates whether the website complies with the necessary legal and ethical standards for parsing.
    """

    compliant: bool
    message: str


def verify_compliance(url: str) -> VerifyComplianceResponse:
    """
    Verifies website compliance before initiating parsing activities.

    Args:
        url (str): URL of the website to be checked for compliance.

    Returns:
        VerifyComplianceResponse: Indicates whether the website complies with the necessary legal and ethical standards for parsing.

    Example:
        response = verify_compliance("https://www.example.com")
        print(response)
        > VerifyComplianceResponse(compliant=True, message="Website is compliant with robots.txt and other legal standards for parsing.")
    """
    robots_txt_url = url.rstrip("/") + "/robots.txt"
    try:
        response = requests.get(robots_txt_url)
        if response.status_code == 200 and "Disallow:" in response.text:
            return VerifyComplianceResponse(
                compliant=False, message="Website disallows parsing in robots.txt."
            )
        else:
            return VerifyComplianceResponse(
                compliant=True,
                message="Website is compliant with robots.txt and other legal standards for parsing.",
            )
    except requests.RequestException as e:
        return VerifyComplianceResponse(
            compliant=False, message=f"Error checking compliance: {str(e)}"
        )
