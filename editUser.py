import accountManager

text = 0

username = input("Enter the username of the user you want to edit: ")

while text != 10:
    print("Choose an option: ")
    print("1: Set user as an admin")
    print("2: View an user's email")
    print("3: View a user's hashed password")
    print("4: Remove admin status of user")
    print("10: Exit")
    try:
        text = int(input())
    except Exception as e:
        print("Please enter a number")

    for i in accountManager.accounts:
        if i.username == username: 
            if text == 1:
                i.admin = True
            elif text == 2:
                print(i.email)
            elif text == 3:
                print(i.password)
            elif text == 4:
                i.admin = False
            else:
                print("Enter a valid option")
    if text == 10:
        accountManager.saveAccounts()
        break