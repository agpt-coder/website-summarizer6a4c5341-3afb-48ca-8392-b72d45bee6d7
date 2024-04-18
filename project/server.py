import logging
from contextlib import asynccontextmanager
from typing import List, Optional

import project.check_parsing_status_service
import project.create_session_service
import project.initiate_parsing_service
import project.retrieve_results_interface_service
import project.retrieve_summary_service
import project.send_for_summarization_service
import project.start_parsing_interface_service
import project.terminate_session_service
import project.update_parsing_strategy_service
import project.verify_compliance_service
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response
from prisma import Prisma

logger = logging.getLogger(__name__)

db_client = Prisma(auto_register=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_client.connect()
    yield
    await db_client.disconnect()


app = FastAPI(
    title="Website summarizer",
    lifespan=lifespan,
    description="To develop a website parser that parses all pages of a given website and sends the extracted information to Claude 3 Opus for content summarization, follow these comprehensive steps using the recommended tech stack (Python, FastAPI, PostgreSQL, and Prisma):\n\n1. **Environment Setup**: Ensure Python is installed on your system. Setup a virtual environment for your project to manage dependencies effectively. Utilize 'pip' to install FastAPI, Uvicorn (for serving FastAPI applications), Prisma Client Python, and other necessary libraries such as BeautifulSoup or lxml for HTML parsing, and requests for managing HTTP requests.\n\n2. **FastAPI Application**:\n   - Start by creating a new FastAPI application. Import FastAPI and instantiate an app object.\n   - Define endpoints for initiating the website parsing process and for receiving summarized content.\n\n3. **Website Parsing**:\n   - Choose a web parsing library like BeautifulSoup or lxml. These libraries facilitate extracting content from HTML/XML documents.\n   - Implement a function to recursively crawl all pages of the website. You may need to manage relative and absolute URLs and consider handling pagination or JavaScript-generated content as needed.\n   - For each page, extract the desired information based on your criteria—text, images, links, etc.\n\n4. **Content Summarization**:\n   - After parsing the web pages, format the extracted information into a suitable structure for summarization.\n   - This structured data can then be sent to Claude 3 Opus. Depending on the integration method, this might be via an API call where the data is sent in the request body.\n\n5. **Database Storage with PostgreSQL and Prisma**:\n   - Use PostgreSQL to store the parsed and summarized content. Design your database schema to effectively represent the information extracted from the website and the summaries from Claude 3 Opus.\n   - Integrate Prisma by defining your database schema in `schema.prisma`. Then, use Prisma Client in your FastAPI app to interact with PostgreSQL, performing operations like insertions and queries.\n\n6. **Testing and Deployment**:\n   - Thoroughly test your application to ensure it correctly parses websites, extracts information, and retrieves summaries. Consider unit and integration tests.\n   - Deploy your FastAPI application using a cloud provider or a server of your choice. Ensure the deployment environment has access to a PostgreSQL database.\n\n7. **Legal and Ethical Considerations**:\n   - Always respect the `robots.txt` file of the target website to check for crawling and scraping permissions. Additionally, be mindful of copyright and intellectual property laws, and ensure your use case complies with legal requirements.\n\nThis approach combines Python for scripting, FastAPI for web application development, PostgreSQL for data persistence, and Prisma for ORM, covering the entire workflow from website parsing to summarization with Claude 3 Opus.",
)


@app.get(
    "/compliance/check/{url}",
    response_model=project.verify_compliance_service.VerifyComplianceResponse,
)
async def api_get_verify_compliance(
    url: str,
) -> project.verify_compliance_service.VerifyComplianceResponse | Response:
    """
    Verifies website compliance before initiating parsing activities.
    """
    try:
        res = project.verify_compliance_service.verify_compliance(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/summarize/send",
    response_model=project.send_for_summarization_service.SummarizeContentResponse,
)
async def api_post_send_for_summarization(
    content: str, context: Optional[str], language: str
) -> project.send_for_summarization_service.SummarizeContentResponse | Response:
    """
    Sends parsed content data to Claude 3 Opus for summarization.
    """
    try:
        res = await project.send_for_summarization_service.send_for_summarization(
            content, context, language
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.delete(
    "/session/end/{sessionId}",
    response_model=project.terminate_session_service.TerminateSessionResponse,
)
async def api_delete_terminate_session(
    sessionId: str,
) -> project.terminate_session_service.TerminateSessionResponse | Response:
    """
    Terminates an existing session based on session ID.
    """
    try:
        res = await project.terminate_session_service.terminate_session(sessionId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/interface/start",
    response_model=project.start_parsing_interface_service.StartParsingInterfaceResponse,
)
async def api_get_start_parsing_interface(
    url: str,
) -> project.start_parsing_interface_service.StartParsingInterfaceResponse | Response:
    """
    Provides an interface for users to submit websites for parsing.
    """
    try:
        res = await project.start_parsing_interface_service.start_parsing_interface(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/parse/start/{url}",
    response_model=project.initiate_parsing_service.InitiateParsingResponse,
)
async def api_post_initiate_parsing(
    url: str,
) -> project.initiate_parsing_service.InitiateParsingResponse | Response:
    """
    Starts the website parsing process for a given URL.
    """
    try:
        res = await project.initiate_parsing_service.initiate_parsing(url)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.put(
    "/adaptability/update",
    response_model=project.update_parsing_strategy_service.UpdateParsingStrategyResponse,
)
async def api_put_update_parsing_strategy(
    website_id: str,
    changed_elements: List[
        project.update_parsing_strategy_service.WebsiteElementChange
    ],
    additional_notes: Optional[str],
) -> project.update_parsing_strategy_service.UpdateParsingStrategyResponse | Response:
    """
    Updates parsing strategies based on detected changes in website layouts.
    """
    try:
        res = await project.update_parsing_strategy_service.update_parsing_strategy(
            website_id, changed_elements, additional_notes
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/parse/status/{taskId}",
    response_model=project.check_parsing_status_service.ParsingStatusResponse,
)
async def api_get_check_parsing_status(
    taskId: str,
) -> project.check_parsing_status_service.ParsingStatusResponse | Response:
    """
    Checks the status of the parsing process for a given task ID.
    """
    try:
        res = await project.check_parsing_status_service.check_parsing_status(taskId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/interface/results/{taskId}",
    response_model=project.retrieve_results_interface_service.ResultsOutput,
)
async def api_get_retrieve_results_interface(
    taskId: str,
) -> project.retrieve_results_interface_service.ResultsOutput | Response:
    """
    Provides an interface to access summarization results.
    """
    try:
        res = (
            await project.retrieve_results_interface_service.retrieve_results_interface(
                taskId
            )
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.get(
    "/summarize/retrieve/{taskId}",
    response_model=project.retrieve_summary_service.SummaryResponse,
)
async def api_get_retrieve_summary(
    taskId: str,
) -> project.retrieve_summary_service.SummaryResponse | Response:
    """
    Retrieves summarized content for a given task ID.
    """
    try:
        res = await project.retrieve_summary_service.retrieve_summary(taskId)
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )


@app.post(
    "/session/start",
    response_model=project.create_session_service.CreateSessionResponse,
)
async def api_post_create_session(
    username: str, password: str, website_url: str
) -> project.create_session_service.CreateSessionResponse | Response:
    """
    Initiates a new session for a website that requires authentication.
    """
    try:
        res = await project.create_session_service.create_session(
            username, password, website_url
        )
        return res
    except Exception as e:
        logger.exception("Error processing request")
        res = dict()
        res["error"] = str(e)
        return Response(
            content=jsonable_encoder(res),
            status_code=500,
            media_type="application/json",
        )
