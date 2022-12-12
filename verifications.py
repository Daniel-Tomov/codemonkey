
verifications = []
class verifications:
    def __init__(self, email):
        self.email = email
        self.token = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + '1234567890', k=20))
        self.isVerified = False
        verifications.append(self)

    def isVerified(self):
        return self.isVerified


def getVerification(email):
    if email == "":
        return None

    for i in verifications:
        if i.email == email:
            return i