---
date: 2024-04-18T06:13:43.449827
author: AutoGPT <info@agpt.co>
---

# Website summarizer

To develop a website parser that parses all pages of a given website and sends the extracted information to Claude 3 Opus for content summarization, follow these comprehensive steps using the recommended tech stack (Python, FastAPI, PostgreSQL, and Prisma):

1. **Environment Setup**: Ensure Python is installed on your system. Setup a virtual environment for your project to manage dependencies effectively. Utilize 'pip' to install FastAPI, Uvicorn (for serving FastAPI applications), Prisma Client Python, and other necessary libraries such as BeautifulSoup or lxml for HTML parsing, and requests for managing HTTP requests.

2. **FastAPI Application**:
   - Start by creating a new FastAPI application. Import FastAPI and instantiate an app object.
   - Define endpoints for initiating the website parsing process and for receiving summarized content.

3. **Website Parsing**:
   - Choose a web parsing library like BeautifulSoup or lxml. These libraries facilitate extracting content from HTML/XML documents.
   - Implement a function to recursively crawl all pages of the website. You may need to manage relative and absolute URLs and consider handling pagination or JavaScript-generated content as needed.
   - For each page, extract the desired information based on your criteria—text, images, links, etc.

4. **Content Summarization**:
   - After parsing the web pages, format the extracted information into a suitable structure for summarization.
   - This structured data can then be sent to Claude 3 Opus. Depending on the integration method, this might be via an API call where the data is sent in the request body.

5. **Database Storage with PostgreSQL and Prisma**:
   - Use PostgreSQL to store the parsed and summarized content. Design your database schema to effectively represent the information extracted from the website and the summaries from Claude 3 Opus.
   - Integrate Prisma by defining your database schema in `schema.prisma`. Then, use Prisma Client in your FastAPI app to interact with PostgreSQL, performing operations like insertions and queries.

6. **Testing and Deployment**:
   - Thoroughly test your application to ensure it correctly parses websites, extracts information, and retrieves summaries. Consider unit and integration tests.
   - Deploy your FastAPI application using a cloud provider or a server of your choice. Ensure the deployment environment has access to a PostgreSQL database.

7. **Legal and Ethical Considerations**:
   - Always respect the `robots.txt` file of the target website to check for crawling and scraping permissions. Additionally, be mindful of copyright and intellectual property laws, and ensure your use case complies with legal requirements.

This approach combines Python for scripting, FastAPI for web application development, PostgreSQL for data persistence, and Prisma for ORM, covering the entire workflow from website parsing to summarization with Claude 3 Opus.

## What you'll need to run this
* An unzipper (usually shipped with your OS)
* A text editor
* A terminal
* Docker
  > Docker is only needed to run a Postgres database. If you want to connect to your own
  > Postgres instance, you may not have to follow the steps below to the letter.


## How to run 'Website summarizer'

1. Unpack the ZIP file containing this package

2. Adjust the values in `.env` as you see fit.

3. Open a terminal in the folder containing this README and run the following commands:

    1. `poetry install` - install dependencies for the app

    2. `docker-compose up -d` - start the postgres database

    3. `prisma generate` - generate the database client for the app

    4. `prisma db push` - set up the database schema, creating the necessary tables etc.

4. Run `uvicorn project.server:app --reload` to start the app

## How to deploy on your own GCP account
1. Set up a GCP account
2. Create secrets: GCP_EMAIL (service account email), GCP_CREDENTIALS (service account key), GCP_PROJECT, GCP_APPLICATION (app name)
3. Ensure service account has following permissions: 
    Cloud Build Editor
    Cloud Build Service Account
    Cloud Run Developer
    Service Account User
    Service Usage Consumer
    Storage Object Viewer
4. Remove on: workflow, uncomment on: push (lines 2-6)
5. Push to master branch to trigger workflow
