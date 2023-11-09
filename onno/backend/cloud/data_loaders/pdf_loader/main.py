from pathlib import Path
from llama_index import download_loader
from pdf_scrapers import PDFLoader
import openai_utils

import functions_framework

@functions_framework.http
def pdf_loader(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    # Parse the request
    try:
        request_json = request.get_json(silent=False)
        username = request_json['username']
        library = request_json['library']
        pdf = request_json['pdf']
        user_metadata = request_json['user_metadata']
    except:
        return "Error: Could not parse request JSON", 400

    pdfloader = PDFLoader()
    extracted_texts = pdfloader.scrape(pdf)
    
    
    