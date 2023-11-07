EXTRACT_CLIENT_DETAILS_SYSTEM_MESSAGE = {'role': 'system', 'content': 'Your job is to go through this conversation/text and extract relevant information for a real estate agent in a JSON format. Dont make stuff up, say nothing if its not clear.'}
EXTRACT_CLIENT_DETAILS = [{
    'type': 'function',
    'function': {
        'name': 'extract_client_details',
        'description': 'You are assisting a real estate agent and talking to a potential client. Extract relevant information from the conversation. For any of these, dont output anything if its not clear.', 
        'parameters': {
            'type': 'object', 
            'properties': {
                'client_type': {
                    'type': 'string', 
                    'description': 'What type of client is this? Merely select one of these strings: Buyer, Seller, Renter, Landlord, None (if not clear)'
                },
                'budget': {
                    'type': 'number', 
                    'description': 'What is the client\'s budget? Merely output the number in dollars. Dont output anything if its not clear.'
                },
                'location': {
                    'type': 'string',
                    'description': 'What area/location is the client interested in?'
                },
                'bedrooms': {
                    'type': 'integer',
                    'description': 'How many bedrooms does the client want?'
                },
                'bathrooms': {
                    'type': 'integer',
                    'description': 'How many bathrooms does the client want?'
                },
                'parking': {
                    'type': 'integer',
                    'description': 'How many parking spots does the client want?'
                },
                'amenities': {
                    'type': 'string',
                    'description': 'What amenities does the client want?'
                },
                'language': {
                    'type': 'string',
                    'description': 'What language does the client speak?'
                },
                'email': {
                    'type': 'string',
                    'description': 'What is the client\'s email?'
                },
                'timeline': {
                    'type': 'string',
                    'description': 'What is the client\'s timeline?'
                },
                'reason for moving': {
                    'type': 'string',
                    'description': 'What is the client\'s reason for moving?'
                },
                'current living situation': {
                    'type': 'string',
                    'description': 'What is the client\'s current living situation?'
                },
                'pets': {
                    'type': 'string',
                    'description': 'Does the client have any pets?'
                },
                'preapproval status': {
                    'type': 'string',
                    'description': 'What is the client\'s preapproval status?'
                },
                'school district preferences': {
                    'type': 'string',
                    'description': 'What school district preferences does the client have?'
                },
                'investment intent': {
                    'type': 'string',
                    'description': 'What is the client\'s investment intent?'
                },
                'flexibility': {
                    'type': 'string',
                    'description': 'How flexible is the client? What specific points are they willing to be flexible on?'
                },
                'other': {
                    'type': 'string',
                    'description': 'What other information is relevant?'
                }
            }
            }, 
        }
 }]