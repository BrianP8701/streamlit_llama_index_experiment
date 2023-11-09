CHOOSE_BEST_SAMPLE_SYSTEM_MESSAGE = {'role': 'system', 'content': ''}
CHOOSE_BEST_SAMPLE_SCHEMA = [{
    'type': 'function',
    'function': {
        'name': 'choose_best_sample',
        'description': 'We used multiple methods to scrape text from pdfs. Some methods have errors, like strange spacing characters etc. Well provide you with the same text scraped using different methods. Please choose the best sample out of the given numbered samples. Just say the number of the best one.',
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
    }
}]
CHOOSE_BEST_SAMPLE_TOOL = {'type': 'function', 'function': {'name': 'choose_best_sample'}}