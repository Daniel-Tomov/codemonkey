import courseCompletion
import completion
import accountManager

def addAccount(username, email, password):
    account = accountManager.accountManager(username, email, password)
    completion.completion(account.uid)
    courseCompletion.courseCompletion(account.uid)

    # if the data in the challenges.yaml has changed, then add that information to the completion and courseCompletions for the user
    courseCompletion.addNewCourseCompletions()
    completion.addNewCompletions()

    accountManager.saveAccounts()
    courseCompletion.saveCourseCompletions()
    completion.saveCompletions()

    print("Added the user")


while input("Quit? [y]/[n]") != "y":
    username = input("Enter the username for the user: ")
    password = input("Enter the password for the user: ")
    email = input("Enter the email for the user: ")

    for i in accountManager.accounts:
        if i.username == username:
            print("That username already exists!")
            exit(0)

    addAccount(username, email, password)