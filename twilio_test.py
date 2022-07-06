from twilio.twiml.messaging_response import MessagingResponse
from twilio import twiml


# video to do this https://youtu.be/cZeCz_QOoXw

def sms_reply():
    """Respond to incoming calls with a simple text message."""
    # Start our TwiML response
    resp = MessagingResponse()
    
    # Add a message
    resp.message("The Robots are coming! Head for the hills!")

    return str(resp)

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
from twilio.rest import Client



ACCOUNT_SID = 'AC07f9df720f406836bf36885a0795dd66'
TWILIO_AUTH_TOKEN = 'c5dbc722f8f448bbbfd5197fada23bc5'


client = Client(ACCOUNT_SID, TWILIO_AUTH_TOKEN)

calls = client.calls.list(limit=1)

for record in calls:
    print(type(record.from_))
    
    
# {   
#     "account_sid": "ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "annotation": "billingreferencetag1",
#     "answered_by": "machine_start",
#     "api_version": "2010-04-01",
#     "caller_name": "callerid1",
#     "date_created": "Fri, 18 Oct 2019 17:00:00 +0000",
#     "date_updated": "Fri, 18 Oct 2019 17:01:00 +0000",
#     "direction": "outbound-api",
#     "duration": "4",
#     "end_time": "Fri, 18 Oct 2019 17:03:00 +0000",
#     "forwarded_from": "calledvia1",
#     "from": "+13051416799",
#     "from_formatted": "(305) 141-6799",
#     "group_sid": "GPXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "parent_call_sid": "CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "phone_number_sid": "PNXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "price": "-0.200",
#     "price_unit": "USD",
#     "sid": "CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "start_time": "Fri, 18 Oct 2019 17:02:00 +0000",
#     "status": "completed",
#     "subresource_uris": {
#     "feedback": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Feedback.json",
#     "feedback_summaries": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/FeedbackSummary.json",
#     "notifications": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Notifications.json",
#     "recordings": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Recordings.json",
#     "payments": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Payments.json",
#     "events": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Events.json",
#     "siprec": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Siprec.json",
#     "streams": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Streams.json"
#     },
#     "to": "+13051913581",
#     "to_formatted": "(305) 191-3581",
#     "trunk_sid": "TKXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
#     "uri": "/2010-04-01/Accounts/ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX/Calls/CAXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.json",
#     "queue_time": "1000"
# },