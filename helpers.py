import os
import datetime
import json
import logging
from azure.storage.blob import BlobServiceClient
# from FlaskApp import app
from openai import AzureOpenAI
#from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

def insight_extraction(file_content, prompt):
    logging.info(f"file: {file_content}")
    logging.info(f"transcript_prompt: {prompt}")
    # create client for AzureOpenAI
    client = AzureOpenAI(
    azure_endpoint = os.environ.get("AZURE_ENDPOINTS"), 
    api_key=os.environ.get("API_KEY") ,  
    api_version= os.environ.get("API_VERSION")
)
    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": file_content}
    ]

    if not file_content:
        raise ValueError("The 'file' parameter is empty.")
    if not prompt:
        raise ValueError("The 'transcript_prompt' parameter is empty.")
    
    response = client.chat.completions.create(
        model="gpt-4turbo", 
        response_format={
            "type": 'json_object'
        },
        messages = messages,
        temperature=0.95,
        max_tokens=800,
        top_p=0.80,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
        
    )

    output_json = response.choices[0].message.content
    print(output_json.encode('utf-8'))

     # Get the date and time information
    now = datetime.datetime.now()

    # Write the output into the file
    file_name = f"Jsonoutput_{now.strftime('%Y-%m-%d_%H%M%S')}.json"
    
    # Upload to blob Storage 
    connection_string = os.environ.get("BLOB_STORAGE_CONNEC_STRING")
    container_name = os.environ.get("StorageOutputContainerName")
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
    blob_client.upload_blob(output_json.encode('utf-8'))
    print("Uploaded "+ file_name+ " file")

    return(output_json.encode('utf-8'))
