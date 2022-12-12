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
        print("connected")
        smtp_server.ehlo()
        print("ehlo")
        print(codemonkeyEmail)
        print(codemonkeyPassword)
        smtp_server.login(codemonkeyEmail, codemonkeyPassword)
        print("login")
        smtp_server.sendmail(sent_from, to, email_text)
        print("send")
        smtp_server.close()
        print ("Email sent successfully!")
    except Exception as ex:
        print ("Something went wrong….",ex)


if __name__ == "__main__":
    sendEmail(sent_from, "test lol")