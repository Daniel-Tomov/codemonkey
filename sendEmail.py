import smtplib
import os
from dotenv import load_dotenv
load_dotenv()


codemonkeyEmail = 'daniel308712@gmail.com'
codemonkeyPassword = os.getenv('emailPassword')

to = 'daniel308712@gmail.com'
subject = 'insert subject here'
exampleBody = 'insert body here'

def sendEmail(userEmail, subject, body=None):
    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.ehlo()
        smtp_server.login(codemonkeyEmail, codemonkeyPassword)
        
        if body == None:
            message = 'Subject: {}\n\n{}'.format(subject, exampleBody)
        else:
            message = 'Subject: {}\n\n{}'.format(subject, body)

        smtp_server.sendmail(codemonkeyEmail, userEmail, message)
        
        smtp_server.close()
    except Exception as ex:
        print ("Something went wrong….",ex)


if __name__ == "__main__":
    sendEmail(to,'a subject', "test lol")