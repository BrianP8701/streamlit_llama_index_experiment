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

# Your conversation string goes here
conversation_string = """
**Chatbot**: Hello there! I'm Alex, your virtual real estate assistant. How may I assist you in your property journey today? 😊

**Lead**: Hi, I look for home.

**Chatbot**: That's great to hear! Are you looking to buy a home, sell one, or perhaps rent?

**Lead**: Buy home. Not too big.

**Chatbot**: Perfect! Buying a new home is an exciting step. Do you have a specific area you're interested in?

**Lead**: Yes, like place with good school. Maybe Queens?

**Chatbot**: Queens is a wonderful area with many great schools. What is your budget for this purchase?

**Lead**: Budget maybe 500,000 dollar. Is okay?

**Chatbot**: Absolutely, we can work with that. How many bedrooms and bathrooms are you looking for?

**Lead**: Two room good. Two bathroom.

**Chatbot**: Got it, two bedrooms and two bathrooms. Are there any other specific details or features you're looking for in your new home?

**Lead**: I like quiet street. And maybe space for car.

**Chatbot**: A quiet street and a parking space, understood. One last question: Are you currently working with a real estate agent or are you just getting started?

**Lead**: Just start. No agent yet.

**Chatbot**: No problem at all. I can help guide you through the process. If you'd like, I can schedule a time for you to speak with one of our top agents who is very familiar with Queens and can speak Korean. Would you prefer a phone call or a video chat?

**Lead**: Oh, Korean good. Video chat good, thank you.

**Chatbot**: You're welcome! Could you please provide me with a preferred date and time for the video chat? Our agent will be ready to discuss all the details with you and help you find the perfect home.

**Lead**: This Saturday afternoon?

**Chatbot**: Saturday afternoon works. I'll arrange everything and send a confirmation email with the details. Could I have your email address, please?

**Lead**: Yes, [koreanlead@email.com](mailto:koreanlead@email.com).

**Chatbot**: Perfect! I've scheduled your appointment, and you'll receive an email shortly. Is there anything else I can assist you with today?

**Lead**: No, very thanks for help!

**Chatbot**: You're very welcome! We're looking forward to helping you find your new home. Have a wonderful day! 🏡✨
"""

# Convert the string into messages list
messages = extract_messages(conversation_string)
print(messages)
