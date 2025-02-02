
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

import mailjet_rest

# def send_email(subject, body, to_address, from_address=None, password=None, smtp_server='smtp.gmail.com', port=587):
#     from_address = os.environ.get("EMAIL_ADDR", from_address)
#     password = os.environ.get("EMAIL_PW", password)
#     smtp_server = os.environ.get("EMAIL_SERVER", smtp_server)
#     port = int(os.environ.get("EMAIL_PORT", port))

#     msg = MIMEMultipart()
#     msg['Subject'] = subject
#     msg['From'] = from_address
#     msg['To'] = to_address

#     msg.attach(MIMEText(body, 'html'))

#     try:
#         #TODO: Fix this - sends 'Connection unexpectedly closed' error
#         #https://stackoverflow.com/questions/28949303/python-smtp-connect-does-not-connect
#         with smtplib.SMTP(smtp_server, port) as server:
#             server.starttls() # not supported by aol
#             # print("Logging in...")
#             server.login(from_address, password)
#             # print("Sending email...")
#             server.sendmail(from_address, to_address, msg.as_string())
#             print(f"Email sent to successfully to {to_address}...")
#             server.quit()
#         # Erfolgreich versendet
#         return True
#     except Exception as e:
#         # Fehler beim Versenden
#         return e

def send_email(subject, body, to_address):

    API_KEY = os.environ.get('MJ_APIKEY_PUBLIC')
    API_SECRET = os.environ.get('MJ_APIKEY_PRIVATE')

    if not API_KEY or not API_SECRET:
        return None

    mailjet_client = mailjet_rest.Client(auth=(API_KEY, API_SECRET), version='v3.1')

    data = {
        'Messages': [
            {
            "From": {
                "Email": "test@gmail.com",
                "Name": "Flask Template"
            },
            "To": [
                {
                "Email": f"{to_address}",
                "Name": "Dich"
                }
            ],
            "Subject": f"{subject}",
            "HTMLPart": f"{body}"
            }
        ]
    }
    result = mailjet_client.send.create(data=data)
    print(result.status_code)
    
    return result.ok


def send_template(subject, template_id, to_address):

    API_KEY = os.environ.get('MJ_APIKEY_PUBLIC')
    API_SECRET = os.environ.get('MJ_APIKEY_PRIVATE')

    if not API_KEY or not API_SECRET:
        return None

    mailjet_client = mailjet_rest.Client(auth=(API_KEY, API_SECRET), version='v3.1')

    data = {
        'Messages': [
            {
                "From": {
                "Email": "test@gmail.com",
                "Name": "Flask Template"
                },
                "To": [
                    {
                    "Email": f"{to_address}",
                    "Name": "You"
                    }
                ],
                "TemplateID": template_id,
                "TemplateLanguage": True,
                "Subject": f"{subject}"
            }
        ]
    }
    result = mailjet_client.send.create(data=data)
    print(result.status_code)
    
    return result.ok