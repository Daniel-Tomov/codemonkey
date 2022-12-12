import random
import string
import sendEmail



verificationsList = ["f"]

class verifications:
    def __init__(self, username, email, password):
        global verifications
        self.username = username
        self.email = email
        self.password = password
        self.token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
        self.isVerified = False
        self.emailSent = False
        verificationsList.append(self)

    def isVerified(self):
        return self.isVerified


def getVerification(email):
    if email == "":
        return None

    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.email == email:
            print(i.email)
            return i

def sendVerification():
    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.emailSent == False:
            print(i.email)
            sendEmail.sendEmail(i.username, "Verify email for Codemonkey")