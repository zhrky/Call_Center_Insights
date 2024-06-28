# Call Center Insights Application

This repository contains an Azure Function App designed to provide insights from call center transcripts. The application leverages Azure OpenAI for natural language processing and Azure Blob Storage for file storage. 

## Features

- **Welcome Page**: A landing page with a welcome message and a link to start the process.
- **Upload Page**: Allows users to upload JSON transcript files or WAV audio files.
- **Extraction Page**: Processes the uploaded transcript file and extracts insights using Azure OpenAI.
- **Blob Storage Integration**: Stores uploaded files and generated JSON output in Azure Blob Storage.

## Setup

### Prerequisites

- Azure subscription
- Azure Function App
- Azure Blob Storage
- Azure OpenAI

### Configuration

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Set up environment variables**:

   Ensure the following environment variables are set in your Azure Function App configuration:
   - `AZURE_ENDPOINTS`: Your Azure OpenAI endpoint.
   - `API_KEY`: Your Azure OpenAI API key.
   - `API_VERSION`: Azure OpenAI API version.
   - `BLOB_STORAGE_CONNEC_STRING`: Connection string for Azure Blob Storage.

### Dependencies

Install the necessary Python packages:
```bash
pip install azure-functions azure-storage-blob openai requests
```

## File Structure

- `function_app.py`: Main application file containing HTTP-triggered functions and routes.
- `helpers.py`: Helper functions for processing transcripts and interacting with Azure Blob Storage.

## Functions

### Welcome Page

Route: `/api/Welcomepage`

Displays a welcome page with a background image and a link to start the process.

### Upload Page

Route: `/api/Uploadpage`

Provides a form for uploading JSON transcript files or WAV audio files, along with a text prompt.

### Extraction Page

Route: `/api/Extractionpage`

Handles the extraction of insights from the uploaded transcript file using Azure OpenAI.

### Helper Functions

- `upload_json_file(req: func.HttpRequest) -> func.HttpResponse`: Handles the upload of JSON files to Azure Blob Storage.
- `insight_extraction(file_content, prompt)`: Processes the transcript and extracts insights using Azure OpenAI.

## Usage

1. **Navigate to the Welcome Page**: 
   ```
   <your-function-app-url>/api/Welcomepage
   ```
2. **Start the Process**: Click the "Let's Start" button to navigate to the Upload Page.
3. **Upload Files**: Choose a transcript JSON file or a WAV audio file, enter a prompt, and submit.
4. **View Results**: The Extraction Page will display the uploaded content and the extracted insights.

## Notes

- Ensure all necessary Azure resources (Function App, Blob Storage, OpenAI) are correctly configured and accessible.
- Update the `connection_string` and other configuration settings as per your Azure setup.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

