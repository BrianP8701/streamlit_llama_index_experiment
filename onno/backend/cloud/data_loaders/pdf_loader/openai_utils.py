import openai
import warnings
import json
from google.cloud import secretmanager

def access_secret():
    # Create the Secret Manager client.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret.
    name = f"projects/onno/secrets/openai_api_key/versions/latest"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Return the decoded payload of the secret.
    secret_string = response.payload.data.decode("UTF-8")
    return secret_string

openai.api_key = access_secret()

CHOOSE_BEST_SCRAPED_TEXT =    '''We used multiple methods to scrape text from pdfs. Some methods 
have errors, like strange spacing characters etc. We'll provide you with the same text scraped using
different methods. Please choose the best sample out of the given numbered samples. Just say the number 
of the best one.'''

CHOOSE_BEST_SAMPLE = [{
        'name': 'choose_best_sample',
        'description': CHOOSE_BEST_SCRAPED_TEXT, 
        'parameters': {
            'type': 'object', 
            'properties': {
                'best_sample': {
                    'type': 'integer', 
                    'description': 'Provide the number of the sample that you think is best formatted. (No spacing errors, no missing characters, etc.)'
                }
            }, 
            'required': ['indexed_text']
        }
 }]

def function_call_with_gpt3_turbo(messages, functions, function_call='auto', temperature=0.0):
    if type(messages) == str: # In case someone accidentally passes in a string instead of a list of messages
        warnings.warn("chat_with_gpt3_turbo() expects a list of messages, not a string.")
        messages = [{"role": "user", "content": messages}]
    for message in messages:
        message["content"] = message["content"].encode('latin-1', errors='ignore').decode('latin-1')
    completion = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k',messages=messages,temperature=temperature,functions=functions, function_call=function_call)
    return completion

def choose_best_scraped_text(samples):
    '''
        When using pdf scrapers, sometimes noise can happen. Here we ask ChatGPT 
        to choose the best sample from a list of samples.
        
        Args:
        - samples (list): List of sample from each scraper. Each sample is a string.
    '''
    user_prompt = ''
    index = 1
    for sample in samples:
        user_prompt += f'{index}: {sample}\n'
    messages = [{"role": "user", "content": user_prompt}]
    response = function_call_with_gpt3_turbo(messages, CHOOSE_BEST_SAMPLE, function_call={'name':'choose_best_sample'}).choices[0]['message']['function_call']['arguments']
    return(json.loads(response)['best_sample'])