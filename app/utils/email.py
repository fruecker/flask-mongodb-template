
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib


def send_email(subject, body, to_address, from_address=None, password=None, smtp_server='smtp.gmail.com', port=587):
    from_address = os.environ.get("EMAIL_ADDR", from_address)
    password = os.environ.get("EMAIL_PW", password)
    smtp_server = os.environ.get("EMAIL_SERVER", smtp_server)
    port = int(os.environ.get("EMAIL_PORT", port))

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_address
    msg['To'] = to_address

    msg.attach(MIMEText(body, 'html'))

    try:
        #TODO: Fix this - sends 'Connection unexpectedly closed' error
        #https://stackoverflow.com/questions/28949303/python-smtp-connect-does-not-connect
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls() # not supported by aol
            # print("Logging in...")
            server.login(from_address, password)
            # print("Sending email...")
            server.sendmail(from_address, to_address, msg.as_string())
            print(f"Email sent to successfully to {to_address}...")
            server.quit()
        # Erfolgreich versendet
        return True
    except Exception as e:
        # Fehler beim Versenden
        return e