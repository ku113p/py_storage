# PDF File Uploader

A simple FastAPI application to upload and download PDF files.

## Features

*   Upload PDF files.
*   Download PDF files.

## Getting Started

### Prerequisites

*   Python 3.13 or later.
*   Docker (optional, for containerized deployment).

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    cd <repository-name>
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

### Running the Application

Run the FastAPI application using Uvicorn:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### API Endpoints

*   **`GET /{path}/upload`**
    *   Displays an HTML form to upload a PDF file to the specified path.
    *   The file will be stored in the `storage/{path}/` directory.
*   **`POST /{path}/upload`**
    *   Uploads a PDF file to the specified path.
    *   The request body should be `multipart/form-data` with a `file` field containing the PDF.
    *   The file will be stored in the `storage/{path}/` directory.
*   **`GET /{path}`**
    *   Downloads the PDF file located at `storage/{path}/`.
    *   If multiple files exist in the directory, it will return an error. It expects a single file per path.

## Deployment (Docker)

You can also run the application using Docker.

1.  **Build the Docker image:**
    ```bash
    docker build -t pdf-uploader .
    ```
2.  **Run the Docker container:**
    ```bash
    docker run -p 8000:8000 -v ./storage:/app/storage pdf-uploader
    ```
    This will mount a local `./storage` directory to the container's `/app/storage` directory, so uploaded files persist on the host machine.

## Project Structure

```
.
├── Dockerfile          # Defines the Docker image
├── main.py             # FastAPI application code
├── requirements.txt    # Python dependencies
└── storage/            # Default directory for storing uploaded PDFs (created automatically)
```
