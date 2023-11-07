import re

def extract_messages(convo_string):
    '''
    Takes in a string like:
        **Chatbot**: Hello! Welcome to QuickFind Homes. How can I assist you in finding the perfect property today?
        **Lead**: hi... i look house. big place. maybe you help?
        ...
        **Chatbot**: You're welcome! I'll get that information to you shortly. If you have any questions in the meantime, don't hesitate to reach out. Have a great day!
    And returns a valid messages list to be passed into ChatGPT.
    '''
    # Split the string by lines
    lines = convo_string.split('\n\n')
    messages = []

    # Regex patterns for identifying roles
    chatbot_pattern = r"^\*\*Chatbot\*\*: "
    lead_pattern = r"^\*\*Lead\*\*: "

    for line in lines:
        # Clean up the line
        line = line.strip()

        # Check if the line belongs to Chatbot
        if re.match(chatbot_pattern, line):
            content = re.sub(chatbot_pattern, '', line)
            messages.append({"role": "assistant", "content": content})

        # Check if the line belongs to Lead
        elif re.match(lead_pattern, line):
            content = re.sub(lead_pattern, '', line)
            messages.append({"role": "user", "content": content})

    return messages