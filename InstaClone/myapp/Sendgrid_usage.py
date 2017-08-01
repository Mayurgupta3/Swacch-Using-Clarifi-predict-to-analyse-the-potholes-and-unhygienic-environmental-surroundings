# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *



def send_response(message_payload):
    sg = sendgrid.SendGridAPIClient(apikey='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')
    response = sg.client.mail.send.post(request_body=message_payload)
    print(response.status_code)
    print(response.body)
    print(response.headers)

