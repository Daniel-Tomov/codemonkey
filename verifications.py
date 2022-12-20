import random
import string
import sendEmail
import personalFunctions


verifyTimeout = {"hours": 0, "minutes": 5, "seconds": 0}
verificationsList = ["f"]

class verifications:
    def __init__(self, username, email, password):
        global verifications
        self.username = username
        self.email = email
        self.password = personalFunctions.encrypt(password)
        self.token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
        self.verified = False
        self.emailSent = False
        verificationsList.append(self)
        self.expireTime = personalFunctions.expireTime(verifyTimeout)

    def isVerified(self):
        return self.verified

    def setVerified(self):
        self.verified = True
        verificationsList.remove(self)


def getVerificationByEmail(email):
    if email == "":
        return None

    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.email == email:
            print(i.email)
            return i


def getVerificationByID(id):
    if id == "":
        return None

    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.token == id:
            print(i.email)
            return i


def sendVerification():
    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.emailSent == False:
            print(f'Sent email to {i.email} with id of {i.token}')
            i.emailSent = True
            sendEmail.sendEmail(i.email, subject="Verify Email for Codemonkey", body=f'Verify email for Codemonkey\nYour link is https://codemonkey.tk/verify/{i.token}.')

def removeVerifications():
    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.expireTime < personalFunctions.time():
            verificationsList.remove(i)