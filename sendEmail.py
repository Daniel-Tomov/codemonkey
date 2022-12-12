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
        print("connected")
        
        smtp_server.ehlo()
        print("ehlo")
        
        print(codemonkeyEmail)

        smtp_server.login(codemonkeyEmail, codemonkeyPassword)
        print("login")

        if body == None:
            message = 'Subject: {}\n\n{}'.format(subject, exampleBody)
        else:
            message = 'Subject: {}\n\n{}'.format(subject, body)

        smtp_server.sendmail(codemonkeyEmail, userEmail, message)
        print("send")
        
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


if __name__ == "__main__":
    sendEmail(to,'a subject', "test lol")