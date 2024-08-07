# Call Center Insights Application

This repository contains an Azure Function App designed to provide insights from call center transcripts using Azure OpenAI service. The application leverages Azure OpenAI for natural language processing and Azure Blob Storage for file storage. 

**Project Aim**

Call Center Insights Application is designed for businesses seeking to enhance their call center operations through advanced natural language processing. By leveraging Azure OpenAI and Azure Blob Storage, the application extracts valuable insights from call center transcripts, facilitating improved decision-making and operational efficiency. This tool is particularly beneficial for call center managers, analysts, and customer service teams looking to harness AI technology to optimize performance and customer satisfaction.

## Features

- **Welcome Page**: A landing page with a welcome message and a link to start the process.
- **Upload Page**: Allows users to upload JSON transcript files or WAV audio files.
- **Extraction Page**: Processes the uploaded transcript file and extracts insights using Azure OpenAI(gpt-4o).
- **Blob Storage Integration**: Stores uploaded files and generated JSON output in Azure Blob Storage.

## Architecture

![image](https://github.com/user-attachments/assets/09e2450f-1633-4109-8520-ae3f78c0fc67)

## Get Started

### Prerequisites

- Azure subscription
- [Azure Function App](https://learn.microsoft.com/en-us/azure/azure-functions/)
- [Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/)
- [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- Python
    [Python 3.8+](https://www.python.org/downloads/)
    [Python VS Code extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [Azure Speech Service](https://azure.microsoft.com/en-us/products/ai-services/ai-speech)


Azure Account - If you're new to Azure, get an Azure account for [free](https://azure.microsoft.com/en-us/free/?wt.mc_id=online-social-sicotin)
 and you'll get some free Azure credits to get started.
 
Azure subscription with access enabled for the Azure OpenAI Service - For more details, see the [Azure OpenAI Service documentation on how to get access](https://learn.microsoft.com/en-us/azure/ai-services/openai/overview#how-do-i-get-access-to-azure-openai).

Azure OpenAI resource - For these samples, you'll need to deploy models like GPT-3.5 Turbo, GPT 4, DALL-E, and Whisper. See the Azure OpenAI Service documentation for more details on [deploying models](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal) and [model availability](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models)
.




### Configuration

1. **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

    then open with Visual Studio Code or other IDE

2. **Create the virtual environment (venv)(optional)**:

    ```bash
    python -m venv venv
    ```

-Note: create venv in your directory.

   ![image](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/31bc3cc8-6031-42d5-ac8a-8de4f433ee41)


 Activate virtual environment :
    
- Windows:
  
  ```bash
          venv\Scripts\activate.ps1
   ```
  
- MacOS/Linux:
  
   ```bash
          source venv/bin/activate.ps1
    ```

3. **Set Environment Variables**:

    Ensure the following environment variables are set in your Azure Function App configuration:
    - `AZURE_ENDPOINTS`: Your Azure OpenAI endpoint.
    - `API_KEY`: Your Azure OpenAI API key.
    - `API_VERSION`: Azure OpenAI API version.
    - `BLOB_STORAGE_CONNEC_STRING`: Azure Blob Storage connection string.
    - `AzureWebJobsStorage`: Azure WebJobs storage connection string.
    - `FUNCTIONS_WORKER_RUNTIME`: Python.
    - `AzureWebJobsFeatureFlags`: EnableWorkerIndexing.

Example `local.settings.json` (fill the keyaccording to description in your LOCAL ):

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<your-blob-storage-connection-string>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsFeatureFlags": "EnableWorkerIndexing",
    "BLOB_STORAGE_CONNEC_STRING": "<your-blob-storage-connection-string>",
    "AZURE_ENDPOINTS": "<your-azure-openAI-endpoints>",
    "API_KEY": "<your-azure-openAI-api-key>",
    "API_VERSION": "<your-api-azure-openAI-version>",
    "StorageAccountName": "<your-storage-account-name>",
    "StorageInputContainerName": "<STORAGE-INPUT-CONTAINER-NAME>",
    "StorageOutputContainerName": "<STORAGE-OUTPUT-CONTAINER-NAME>",
    "WelcomeBackgroundSAS": "<welcome-page-background-sas-url>",
    "UploadBackgroundSAS": "<upload-page-background-sas-url>",
    "ExtractionBackgroundSAS": "<extraction-page-background-sas-url>",
    "LogoSAS": "<Brand-logo-sas-url>",
    "LoadingGifSAS": "<loading-gif-sas-url>"
  }
}
```
! please create local.settings.json and copy paste this json examle in it and fill the requirement places

### Dependencies

4. Install the necessary Python packages:

    ```bash
    pip install azure-functions azure-storage-blob openai requests
    ```

    or

    ```bash
    pip install -r requirements.txt
    ```
    
5. Deploy the function App
   
   After fill and run the commands, deploy this app to Azure
   
   -Click azure symbol in VsCode
   
   ![image](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/2b41f06f-05a4-466a-829e-7948d4500dfe)

   -Then create a Function App
   
   ![image](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/ef89d156-136b-41f0-892d-6e5c9608b8ea)

   -Give the name `callcenter-insights`

   -Select `python 3.11`

   -Select region  `sweden central`(optionally you can choose this region)

    Deployment image**

   After succesfully deployed app your function resource look like in Azure. Click browse and try the app : )
   
   

## File Structure

- `function_app.py`: Main application file containing HTTP-triggered functions and routes.
- `helpers.py`: Helper functions for processing transcripts and interacting with Azure Blob Storage.

## Functions

### Welcome Page

Route: `/api/Welcomepage`

Displays a welcome page with a background image and a link to start the process.

![Screenshot 2024-05-22 172303](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/e8746d15-3b8f-4452-9e7d-afd43cce9768)


### Upload Page

Route: `/api/Uploadpage`

Provides a form for uploading JSON transcript files or WAV audio files, along with a text prompt.

![Screenshot 2024-06-28 131210](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/f8fc6005-636e-4609-9463-ecfd86cacdca)


### Extraction Page

Route: `/api/Extractionpage`

Handles the extraction of insights from the uploaded transcript file using Azure OpenAI(gpt-4o).

![Screenshot 2024-05-21 131053](https://github.com/gatttaca01/Call_Center_Insight/assets/78308539/efa7d902-a269-4ca0-80e6-0ff5487ecaaf)


### Helper Functions

- `upload_json_file(req: func.HttpRequest) -> func.HttpResponse`: Handles the upload of JSON files to Azure Blob Storage.
- `insight_extraction(file_content, prompt)`: Processes the transcript and extracts insights using Azure OpenAI.



## Usage

1. After configurations run the functions

2. **Start the Process**: Click the "Let's Start" button to navigate to the Upload Page.
3. **Upload Files**: Choose a transcript JSON file or a WAV audio file, enter a prompt, and submit.
4. **View Results**: The Extraction Page will display the uploaded content and the extracted insights.

## Notes

- Ensure all necessary Azure resources (Function App, Blob Storage, AzurevOpenAI) are correctly configured and accessible.
- Update the `connection_string` and other configuration settings as per your Azure setup.
- please check the azure function supported python version in this scenario I used python 3.11.9

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

