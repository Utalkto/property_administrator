from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml


# video to do tihis https://youtu.be/cZeCz_QOoXw

def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)
