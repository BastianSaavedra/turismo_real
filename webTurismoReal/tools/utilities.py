from django.conf import settings
# Email
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def sendMail(html, subject, to):

    msg = MIMEMultipart('alternative')
    msg['From'] = settings.MAIL_OUTPUT
    msg['To'] = to 
    msg['Subject'] = subject

    msg.attach(MIMEText(html, 'html'))

    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(settings.MAIL_OUTPUT, settings.PASSWORD_MAIL_OUTPUT)
        smtp.sendmail(settings.MAIL_OUTPUT, to, msg.as_string())
        smtp.quit()


def numberFormat(number):
    if number == None:
        return 0
    else:
        return "{:,}".format(number).replace(",",".")
