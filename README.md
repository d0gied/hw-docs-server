# hw-docs-server

## Services

### Storage Service
The storage service is responsible for storing and retrieving documents. It provides an API for uploading, downloading, and managing documents.

- **API Endpoints:**
    - `POST /files`: Upload a new document.
    - `GET /files/{id}`: Download a document by its ID.

### Analysis Service
The analysis service processes documents to extract metadata and perform analysis. It can be used to generate summaries, extract keywords, and more.

- **API Endpoints:**
    - `POST /analytics/{file_id}`: Analyze a document and return metadata.
    - `GET /analytics/{path}`: Retrieve analysis results for a document (by its file path).

### Gateway Service
The gateway service acts as a reverse proxy, routing requests to the appropriate service based on the request path.
- **API Endpoints:**
    - `GET /files/{id}`: Proxy to the storage service to download a document.
    - `POST /files`: Proxy to the storage service to upload a new document.
    - `POST /analytics/{file_id}`: Proxy to the analysis service to analyze a document.
    - `GET /analytics/{path}`: Proxy to the analysis service to retrieve analysis results.


## Development Setup

Each service is a separate Python package. To set up the development environment, follow these steps:
1. Clone the repository:
   ```bash
   git clone github.com/d0gied/hw-docs-server.git
   cd hw-docs-server
   ```
2. Choose a service to work on (e.g., `storage`, `analysis`, or `gateway`).
3. Install a virtual environment:
   ```bash
   poetry install
   ```
4. Setup virtual environment according to the services `config.py` (e.g., `storage/config.py`, `analysis/config.py`, or `gateway/config.py`):
    - it contains `Configz class with fields, that uses `getenv` to read environment variables.
    - getenv(`variable_name`, default_value) will read the environment variable `variable_name` or return `default_value` if it is not set.
    - You can set environment variables in your terminal using `export VARIABLE_NAME=value`.

5. Run the service:
   ```bash
   chmod +x ./run.sh
   ./run.sh
   ```
6. Repeat steps 2-5 for each service you want to work on.

7. Use swagger to test the API endpoints:
   - Navigate to `http://localhost:8000/docs` for the gateway service.
   - Navigate to `http://localhost:8001/docs` for the storage service.
   - Navigate to `http://localhost:8002/docs` for the analysis service.

