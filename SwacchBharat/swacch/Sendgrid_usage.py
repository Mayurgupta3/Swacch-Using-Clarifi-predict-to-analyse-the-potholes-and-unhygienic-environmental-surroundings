# using SendGrid's Python Library
# https://github.com/sendgrid/sendgrid-python
import sendgrid
import os
#from sendgrid.helpers.mail import *

# Calling Sendgrid API's to send email

def send_response(message_payload):
    #sg = sendgrid.SendGridAPIClient(apikey='SG.59Qj2MP0OaynIp4Q.lFpcnD2DKMMb6vRb9Yok090djX8DJPJMREKs8wCA')
    response = sg.client.mail.send.post(request_body=message_payload)
    print("qwerty")
    print(response.status_code)
    print(response.body)
    print(response.headers)

'''
def send_mail(url):
    sg = sendgrid.SendGridAPIClient(apikey='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')

    from_email = Email("sakshikhattar1@gmail.com")
    to_email = Email("Raman007bidhuri@gmail.com")
    message = "<html><body><h1>Image of the dirty area</h1><br><img src =" + url + "></body></html>"
    subject = "Image of dirty area!"
    content = Content("text/html", message)
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)
'''