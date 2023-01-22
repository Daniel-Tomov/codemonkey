import smtplib
import os
from dotenv import load_dotenv
# load the .env which contains the password for the noreply user
load_dotenv()

# the email for the noreply user
codemonkeyEmail = 'noreply@codemonkey.tk'

# the password for the noreply user
# put in .env file for security reasons
codemonkeyPassword = os.getenv('emailPassword')

#print(codemonkeyPassword)

def sendEmail(userEmail, subject, body=None):
    # try to send an email to the user at userEmail
    # this email server is hosted locally on the machine running the backend
    try:
        message = 'Subject: {}\n\n{}'.format(subject, body)

        # setup the SMTP connection
        smtp_server = smtplib.SMTP('mail.codemonkey.tk', 587)
        # connect to the mail server
        smtp_server.starttls()
        smtp_server.login(codemonkeyEmail, codemonkeyPassword)
        #print("logged in")
        
        # send the email
        smtp_server.sendmail(codemonkeyEmail, userEmail, message)
        
        # close the connection
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong….",ex)