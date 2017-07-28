# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
from sendgrid.helpers.mail import *



def send_response(post_url):
    sg = sendgrid.SendGridAPIClient(apikey='SG')
    receipt = "mgupta7042@gmail.com" # Municiplaity email-id
    from_email = Email("uditk53@gmail.com")
    to_email = Email(receipt)
    content_message = "<html><body><img src =" + post_url +  "</body></html>"
    print content_message
    subject = "Image of dirty area"
    content = Content("text/html", content_message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
