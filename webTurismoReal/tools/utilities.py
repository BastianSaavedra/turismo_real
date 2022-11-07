from django.conf import settings
# Email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendMail(html, subject, to):

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = settings.MAIL_OUTPUT
    msg['T'] = to 

    msg.attach(MIMEText(html, 'html'))
    try:
        server = smtplib.SMTP(settings.SERVER_SMTP, settings.PORT_SMTP)
        server.login(settings.MAIL_OUTPUT, settings.PASSWORD_MAIL_OUTPUT)
        server.sendmail(settings.MAIL_OUTPUT, to, msg.as_string())
        server.quit()
    except smtplib.SMTPResponseException as e:
        pass
