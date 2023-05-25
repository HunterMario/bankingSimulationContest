from account import Account
from customExceptions import Breach
from storage import Storage

accounts = Storage.get()

activeAccount = None
while activeAccount == None:
    option1 = input("What would you like to do: \n 1. Sign in \n 2. Create new account \n Enter an option: ")

    # Option to sign into the account
    if "1" in option1 or "sign in" in option1.lower():
        failedAttempts = 0
        accountFound = False
        while not accountFound:
            if failedAttempts >= 3:
                raise Exception("Too many failed login attempts. Please try again later.")
            username = input("Username: ")
            password = input("Password: ")
            for account in accounts:
                if account.username == username:
                    if account.authenticate(password):
                        activeAccount = account
                        accountFound = True
            else:
                if accountFound==False:
                    failedAttempts += 1
                    print("Invalid username or password.")

    # Option to create a new account. This will append the info to the list
    elif "2" in option1 or "create new account" in option1.lower():
        thingsToSay = ["Username: ", "Password: ", "Day of Birth (ex. 21): ", "Month of Birth (1-12): ", "Year of Birth: ", "Street Number: ", "Street Name: ", "City: ", "State: ", "Zip Code: ", "Is compound interest (Yes or No): ", "Interest Rate (Enter as percentage but do not include the percentage sign): "]
        accountInfo = []
        for thing in thingsToSay:
            accountInfo.append(input(thing))
        def determineInterest(info):
            if "y" in info.lower():
                return True
            else:
                return False
        accountInfo[10] = determineInterest(accountInfo[10])
        newAccount = Account(accountInfo[0], accountInfo[1], accountInfo[2], accountInfo[3], accountInfo[4], accountInfo[5], accountInfo[6], accountInfo[7], accountInfo[8], accountInfo[9], accountInfo[10], accountInfo[11])
        accounts.append(newAccount)
        Storage.createNew(newAccount)
        activeAccount = accounts[-1]

    else:
        print("Invalid Input")

programRunning = True
options = ["Make a deposit", "Withdraw", "Transfer", "Apply for a loan", "Pay a loan", "Get Account Statistics", "Change Account Settings", "Log Out"]
while programRunning:
    print("Enter a number representing an option below:")
    optionIndex = 1
    for option in options:
        print(str(optionIndex) + ". " + option)
        optionIndex += 1
    try:
        option2 = int(input("Enter an option: "))
    except ValueError:
        print("Numbers only!")
    try:
        # Option to make a deposit
        if option2 == 1:
            depositAmount = int(input("Enter the amount you would like to deposit: "))
            key = input("Enter your password: ")
            activeAccount.deposit(key, depositAmount)
            print("Successfully deposited $" + str(depositAmount) + " into your account.")
            Storage.update(activeAccount)

        # Option to withdraw money
        elif option2 == 2:
            withdrawAmount = int(input("Enter the amount you would like to withdraw: "))
            key = input("Enter your password: ")
            activeAccount.withdraw(key, withdrawAmount)
            print("Successfully withdrew $" + str(withdrawAmount) + " from your account.")
            Storage.update(activeAccount)

        # Option to transfer money
        elif option2 == 3:
            try:
                accountFound = False
                targetUser = input("Enter the account username you would like to transfer money to: ")
                sourceUserPassword = input("Enter your password: ")
                for account in accounts:
                    if targetUser == account.username:
                        print("Is the following information about the target user accurate:")
                        print("Username: " + account.username)
                        print("ID: " + str(account.id))
                        correctUser = input("Enter an option (yes or no): ")
                        if "y" in correctUser.lower():
                            targetAccount = account
                            accountFound = True
                            break
                if accountFound:
                    amountToTransfer = int(input("How much money would you like to transfer: "))
                    activeAccount.transfer(targetAccount, sourceUserPassword, amountToTransfer)
                else:
                    print("No accounts found with entered username (Note: Usernames are case sensitive)")
            except TypeError:
                print("Amount to transfer must be an integer")
            except Breach:
                print(Breach)
            except ValueError:
                print("Amount being attempted to transfer is greater than source account balance")
        # Option to start a loan
        elif option2 == 4:
            loanAmount = int(input("How much money do you need? "))
            key = input("Enter your password: ")
            activeAccount.loan(key, loanAmount)
            print("Loan successful. You are now $" + str(loanAmount) + " in debt.")
            Storage.update(activeAccount)

        # Option to pay the loan
        elif option2 == 5:
            paidFromAccount = input("Will you be paying this from your account balance? ")
            if "y" in paidFromAccount.lower():
                fromAccount = True
            else:
                fromAccount = False
            payAmount = int(input("How much would you like to pay: "))
            key = input("Enter your password: ")
            activeAccount.payLoan(key, payAmount, fromAccount)
            print("Successfully paid $" + str(payAmount) + " towards your loan.")
            Storage.update(activeAccount)

        elif option2 == 6:
            print("Username: " + activeAccount.username)
            print("Address: " + str(activeAccount.address))
            print("Date Of Birth: " + str(activeAccount.birthDate))
            print("Current Balance: " + str(activeAccount.balance))
            print("Current Debt: " + str(activeAccount.debt))
            print("Current Net Worth: " + str(activeAccount.netWorth()))
            print("Current Interest Rate: " + str(activeAccount.interestRate))

        # Option to change account settings
        elif option2 == 7:
            settingsSelected = True
            while settingsSelected:
                settingOptions = ["Change Username", "Change Password", "Change Address", "Delete Account", "Go Back To Main Menu"]
                settingIndex = 1
                print("Enter a number representing an option below:")
                for option in settingOptions:
                    print(str(settingIndex) + ". " + option)
                    settingIndex += 1
                settingOption = int(input("Enter an option"))
                # Change username
                if settingOption == 1:
                    newUsername = input("Enter a new username: ")
                    activeAccount.username = newUsername
                # Change password
                elif settingOption == 2:
                    try:
                        passwordsMatch = False
                        oldPassword = input("Enter your old password: ")
                        while not passwordsMatch:
                            newPassword = input("Enter your new password: ")
                            newPasswordVerification = input("Reenter your new password: ")
                            if newPassword == newPasswordVerification:
                                passwordsMatch = True
                            else:
                                print("Reentered password different from entered password")
                        activeAccount.setPassword(oldPassword, newPassword)
                    except:
                        print("Old password does not match")
                # Change address
                elif settingOption == 3:
                    try:
                        streetNumber = int(input("Enter Street Number: "))
                        streetName = input("Enter Street Name: ")
                        city = input("Enter City: ")
                        state = input("Enter State: ")
                        zipCode = int(input("Enter Zip Code: "))
                    except ValueError:
                        print(ValueError)
                # Delete Account
                elif settingOption == 4:
                    if activeAccount.netWorth() >= 0:
                        if activeAccount.authenticate(input("Please Enter Your Password: ")):
                            if activeAccount.netWorth > 0:
                                print("You have remaining money in your account. Please withdraw all remaining funds before closing your account.")
                            else:
                                terminationMessage = "By closing my account, I understand that this is a permanent action and that all data inside my account will be lost."
                                userConfirmation = input("This is a permanent action. Please ensure that you are really wanting to do this. If you are, please confirm so by typing the following message below: \n \n By closing my account, I understand that this is a permanent action and that all data inside my account will be lost.")
                                if userConfirmation == terminationMessage:
                                    Storage.deleteAccount(activeAccount)
                                    programRunning = False
                # Go back to main menu
                elif settingOption == 5:
                    settingsSelected = False

        # Option to log out
        elif option2 == 8:
            programRunning = False

        # Default case for invalid input
        else:
            print("Input must be between 1 and " + str((options.len()+1)) + ".")

    except Breach:
        print("Invalid Credentials")
        programRunning = False