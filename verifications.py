import random
import string
import sendEmail
import personalFunctions

# define timeout for verifications
verifyTimeout = {"hours": 0, "minutes": 5, "seconds": 0}

# set the first index of verificationsList to a string because otherwise it does not work
verificationsList = ["_"]

class verifications:
    def __init__(self, username, email, password):
        global verifications
        # define some attributes
        self.username = username
        self.email = email
        # hash the password because it is stored in memory
        self.password = personalFunctions.hash(password)
        self.token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
        # tracks if the user has verified their email
        self.verified = False
        # tracks if the user has been sent an email
        self.emailSent = False
        # sets an expire time for this instance of the verification class
        self.expireTime = personalFunctions.expireTime(verifyTimeout)
        # appends the instance to the verificationsList list
        verificationsList.append(self)
    
    # check if the user is verified
    def isVerified(self):
        return self.verified

    # remove the instance of the class because the user has verified their email
    def setVerified(self):
        verificationsList.remove(self)

# returns the instance of the verification class by an email parameter
def getVerificationByEmail(email):
    if email == "":
        return None
    # iterate over the verificaitonsList
    for i in verificationsList:
        # this is for the string that has to be in the list
        if type(i) == type(""):
            continue
        if i.email == email:
            return i

# returns the instance of the verification class by the ID
def getVerificationByID(id):
    if id == "":
        return None

    # iterate over the verificaitonsList
    for i in verificationsList:
        # this is for the string that has to be in the list
        if type(i) == type(""):
            continue
        if i.token == id:
            return i

# sends verifications to users
def sendVerification():
    # iterate over the verificationsList
    for i in verificationsList:
        # this is for the string that has to be in the list
        if type(i) == type(""):
            continue
        # if the email has not been sent, then send the email
        if i.emailSent == False:
            # message for times when the server the application is being run on does not have the email server installed
            print(f'Sent email to {i.email} with id of {i.token}')
            i.emailSent = True
            
            # send the email. it is commented out because other servers do not have the mail.codemonkey.tk server setup
            #sendEmail.sendEmail(i.email, subject="Verify Email for Codemonkey", body=f'Verify email for Codemonkey\nYour link is https://codemonkey.tk/verify/{i.token}.')

# removes verifications that have expired from the lists
def removeVerifications():
    # iterate over the list
    for i in verificationsList:
        if type(i) == type(""):
            continue
        if i.expireTime < personalFunctions.time():
            verificationsList.remove(i)