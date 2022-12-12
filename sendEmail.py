import smtplib
import os
from dotenv import load_dotenv
load_dotenv()


codemonkeyEmail = '308712@vbstudents.com'
codemonkeyPassword = os.getenv('emailPassword')


sent_from = codemonkeyEmail
to = 'user@gmail.com'
subject = 'Lorem ipsum dolor sit amet'
body = 'consectetur adipiscing elit'

email_text = body

def sendEmail(userEmail, body):
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(codemonkeyEmail, codemonkeyPassword)
        smtp_server.sendmail(sent_from, to, email_text)
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)

sendEmail("308712@vbstudents.com", "test lol")