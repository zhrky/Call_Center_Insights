import azure.functions as func
import logging
import datetime
import json
from azure.storage.blob import BlobServiceClient
import helpers
from openai import AzureOpenAI
import requests
import os



app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="Welcomepage") 
def Welcomepage(req: func.HttpRequest) -> func.HttpResponse:
    
    html_content = """
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            background-image: url('WelcomeBackgroundSAS');
            background-size: cover;
            box-shadow: 0 0 200px rgba(10, 10, 10, 50);
        }
        .welcome-text {
            font-size: 50px;
            text-align: center;
            margin-top: 300px;
            color: #ffffff;
            text-shadow: 5px 5px 5px rgba(2, 2, 2, 5);
            font-family: 'Amasis MT Pro Black', sans-serif;
        }
        .start-button {
            display: block;
            width: 400px;
            margin: 20px auto;
            padding: 20px;
            background-color: #0078D4;
            color: #ffffff;
            text-align: center;
            text-decoration: none;
            border-radius: 15px;
        }
    </style>
</head>
<body>
    <div id="img.logo" text-align:center" >
            <img height="60" src="LogoSAS" />
    </div>
    <div class="welcome-text">Call Center Insight Uygulamasına Hoşgeldiniz</div>
    <a href="https://callcenter-insights.azurewebsites.net/api/Uploadpage" class="start-button">Let's Start</a>
</body>
</html>

    """
    return func.HttpResponse(html_content, mimetype="text/html")


# @app.route('/Extractionpage', methods=['POST'])
@app.route(route="Extractionpage")
def Extractionpage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    

    # file= req.get_body().decode('utf-8')
    file = req.files.get('transcriptFile')
    transcript_prompt = req.form.get('transcriptPrompt')
    #file=req.files
    file_content = file.read().decode('utf-8')
    upload_json_file(file_content)
    # transcript_prompt = req.params.get('transcriptPrompt')
    result = helpers.insight_extraction(file_content, transcript_prompt)
    
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Center Insights Demo</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-image: url('ExtractionBackgroundSAS');
            background-size: cover;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            font-family: 'Times New Roman', Times, serif;
        }}
        .container {{
            text-align: center;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            max-width: 900px;
            width: 100%;
        }}
        h1 {{
            text-align: center;
            color: #0078D4;
            margin-bottom: 20px;
        }}
        .form-section {{
            display: flex;
            justify-content: space-between;
        }}
        .form-container {{
            width: 48%;
            text-align: left;
        }}
        h3 {{
            font-size: 1.2em;
            margin-bottom: 10px;
        }}
        label {{
            display: block;
            margin-bottom: 5px;
        }}
        textarea {{
            width: 100%;
            height: 300px;
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            resize: none;
        }}
        button {{
            width: 100%;
            padding: 10px;
            border: none;
            background-color: #0078D4;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }}
        button:hover {{
            background-color: #005a9e;
        }}
        img.logo {{
            position: absolute;
            top: 10px;
            left: 10px;
        }}
    </style>
    <script>
        document.addEventListener('DOMContentLoaded', function() {{
            var fileContent = {json.dumps(file_content)};
            document.getElementById('transcript').textContent = fileContent;
        }});
    </script>
</head>
<body>
     <div id="logo" text-align="center">
        <img class="logo" height="50" src="LogoSAS" />
    </div>
    <div class="container">
        <h1>Call Center Insights Demo</h1>
        <div class="form-section">
            <div class="form-container">
                <h3>Inputs Preview:</h3>
                <label for="transcript">Transcript:</label>
                <textarea id="transcript" name="transcript"></textarea>
            </div>
            <div class="form-container">
            <h3>Result:</h3>
            <label for="blobContents">Json Output:</label>
            <textarea id="blobContents" readonly>{result.decode('utf-8')}</textarea>
            </div>
        </div>
    </div>
</body>
</html>
        """
    return func.HttpResponse(html_content, mimetype="text/html")


@app.route(route="Uploadpage")
def Uploadpage(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Call Center Insights Demo</title>
    <link rel="icon" type="image/png" href="LogoSAS">
    <style>
        body {
            margin: 0;
            padding: 0;
            background-image: url('UploadBackgroundSAS');
            background-size: cover;
            box-shadow: 0 0 50px rgba(0, 0, 0, 0.8);
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            text-align: center;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            max-width: 900px;
            width: 100%;
        }
        h1 {
            text-align: center;
            color: #0078D4;
        }
        .form-section {
            display: flex;
            justify-content: space-around;
        }
        .form-container {
            width: 45%;
            text-align: left;
        }
        h2 {
            font-size: 1.2em;
            margin-bottom: 10px;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        label {
            margin-bottom: 5px;
            text-align: left;
            width: 100%;
        }
        input[type="file"] {
            margin-bottom: 15px;
            width: 100%;
        }
        textarea {
            width: 100%;
            height: 100px;
            margin-bottom: 15px;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            padding: 10px 15px;
            border: none;
            background-color: #0078D4;
            color: white;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #357ae8;
        }
        img.logo {
            position: absolute;
            top: 10px;
            left: 10px;
        }
        #gif {
            display: none;
            text-align: center;
        }
        #gif img {
            height: 50px;
        }
        #gif h3 {
            margin: 10px 0 0;
        }
        .left-align {
        text-align: left;
        }
    </style>
</head>
<body>
    <div id="logo" text-align="center">
        <img class="logo" height="50" src="LogoSAS" />
    </div>
    <div class="container">
        <h1>Call Center Insights Demo</h1>
        <div class="form-section">
            <div class="form-container">
                <h2>From Transcript:</h2>
                <form id="transcriptForm" action="Extractionpage" method="post" enctype="multipart/form-data">
                    <label for="transcriptFile">Transcript File (.json):</label>
            
                    <input type="file" id="transcriptFile" name="transcriptFile">
                    <label for="transcriptPrompt">Prompt:</label>
                    <textarea id="transcriptPrompt" name="transcriptPrompt" placeholder="You are an AI assistant..."></textarea>
                    <button type="submit" id="transcriptSubmit" onclick="submitForm('transcriptForm', 'transcriptSubmit')">Submit</button> 
</body>
                    </form>
                    
            </div>
            <div class="form-container">
                <h2>From Voice Recording:</h2>
                <form id="voiceForm" action="SpeechToTextpage" method="post" enctype="multipart/form-data">
                    <label for="voiceFile">Speech File (.wav):</label>
                   
                    <input type="file" id="voiceFile" name="voiceFile">
                    <label for="voicePrompt">Prompt:</label>
                    <textarea id="voicePrompt" name="voicePrompt" placeholder="You are an AI assistant..."></textarea>
                    <button type="submit" id="voiceSubmit" onclick="submitForm('voiceForm', 'voiceSubmit')">Submit</button>
                </form>
            </div>
        </div>
        <div id="gif">
            <img src="LoadingGifSAS" />
            <h3>Please wait ...</h3>
        </div>
    </div>
    <script>
        function submitForm(formId, buttonId) {
            var form = document.getElementById(formId);
            var formData = new FormData(form);
            var prompt = formData.get(formId === 'transcriptForm' ? 'transcriptPrompt' : 'voicePrompt');
            formData.append('prompt', prompt);

            var xhr = new XMLHttpRequest();
            xhr.open('POST', form.action, true);
            xhr.onload = function () {
                if (xhr.status === 200) {
                    console.log('Form submission successful');
                } else {
                    console.error('Form submission failed');
                }
                document.getElementById('gif').style.display = 'none';
                document.getElementById('transcriptSubmit').style.display = 'block';
                document.getElementById('voiceSubmit').style.display = 'block';
            };
            xhr.send(formData);
            document.getElementById('gif').style.display = 'block';
            document.getElementById('transcriptSubmit').style.display = 'none';
            document.getElementById('voiceSubmit').style.display = 'none';
        }
    </script>
</body>
</html>
"""
    return func.HttpResponse(html_content, mimetype="text/html")


def upload_json_file(req: func.HttpRequest) -> func.HttpResponse:
    try:
        file_content = req.get_body()
        #upload to input file
        now= datetime.datetime.now()
        file_name = f"Conversation_{now.strftime('%Y-%m-%d_%H%M%S')}.json"
        container_name =  os.environ.get("StorageInputContainerName")
        blob_service_client = BlobServiceClient.from_connection_string("BLOB_STORAGE_CONNEC_STRING")
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=file_name)
        blob_client.upload_blob(file_content)
        return func.HttpResponse(f"Uploaded {file_name} file", status_code=200)
    except Exception as e:
        return func.HttpResponse(f"An error occurred: {str(e)}", status_code=500)
    