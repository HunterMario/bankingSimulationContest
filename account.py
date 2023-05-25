from miscellaneous import Address, DateOfBirth, PasswordSecurity
from customExceptions import Breach, LoanDenied
from loans import Loan
from storage import Storage
import os

def lambdaRaise(exceptionToRaise):
    raise exceptionToRaise

class Account:
    __listOfFiles = (os.listdir(r"C:\Users\hunte\Documents\CodeProjects\bankSimulation\objects"))
    __lastFile = sorted(__listOfFiles)[-1]
    __id = int(__lastFile[0])
    def __init__(self, username, password, dayOfBirth, monthOfBirth, yearOfBirth, addressNumber, streetName, city, state, zipCode, isCompoundInterest, interestRate):
        self.id = Account.__id + 1
        self.username = username
        self.__saltKey = PasswordSecurity.salt()
        self.__password = PasswordSecurity.hash(password, self.__saltKey)
        self.__birthDate = lambda dayOfBirth, monthOfBirth: DateOfBirth(int(dayOfBirth), int(monthOfBirth), int(yearOfBirth)) if (int(dayOfBirth) >= 1 and int(dayOfBirth) <= 32) and (int(monthOfBirth) >= 1 and int(monthOfBirth) <= 12) else lambdaRaise(ValueError)
        self.__address = Address(addressNumber, streetName, city, state, zipCode)
        self.__balance = 0
        self.__interestRate = 0
        self.__isCompoundInterest = isCompoundInterest
        self.__lastBalanceWithoutInterest = 0
        self.__debt = 0
        self.credit = 1
        self.loans = {}
        self.loan_id = 0

    @property
    def password(self):
        return self.__password

    def setPassword(self, oldPassword, newPassword):
        if PasswordSecurity.hash(oldPassword, self.__saltKey) == self.__password:
            self.__password = PasswordSecurity.hash(newPassword, self.__saltKey)
            Storage.update(self)
        else:
            raise Exception("Old password does not match.")

    def authenticate(self, enteredPassword):
        if PasswordSecurity.hash(enteredPassword, self.__saltKey) == self.__password:
            return True
        else:
            return False

    @property
    def address(self):
        return self.__address

    @address.setter
    def address(self, addressNumber, streetName, city, state, zipCode):
        self.__address.streetNumber, self.__address.streetName, self.__address.city, self.__address.state, self.__address.zipCode = addressNumber, streetName, city, state, zipCode
        Storage.update(self)

    @property
    def birthDate(self):
        return self.__birthDate

    # This method only exists for testing reasons and is not used anywhere in the program as someones birthday usually doesn't change.
    def setBirthDate(self, dayOfBirth, monthOfBirth, yearOfBirth):
        if (dayOfBirth >= 1 and dayOfBirth <= 32) and (monthOfBirth >= 1 and monthOfBirth <= 12):
            self.__birthDate.day, self.__birthDate.month, self.__birthDate.year = int(dayOfBirth), int(monthOfBirth), int(yearOfBirth)
            Storage.update(self)
        else:
            raise ValueError("Day of birth or month of birth not in range")

    @property
    def balance(self):
        return self.__balance

    @property
    def debt(self):
        return self.__debt

    @property
    def interestRate(self):
        return self.__interestRate

    # Method that deposits money into a bank account
    def deposit(self, password, amount):
        if PasswordSecurity.hash(password, self.__saltKey) == self.__password:
            self.__balance += amount
            Storage.update(self)
        else:
            raise Breach("Deposit attempted without key")

    # Method that withdraws money from the bank account
    def withdraw(self, password, amount):
        if PasswordSecurity.hash(password, self.__saltKey) == self.__password:
            if self.__balance - amount >= 0:
                self.__balance -= amount
                Storage.update(self)
            else:
                raise ValueError("Withdraw amount greather than account balance")
        else:
            raise Breach("Withdraw attempted without key")

    # Method to add money to account balance (This should only be used by other methods inside the class)
    def __add(self, amount):
        self.__balance += amount

    # Method to subtract money from account balance (This should only be used by other methods inside the class)
    def __subtract(self, amount):
        self.__balance -= amount

    # Method to transfer money from one account to another
    def transfer(self, targetAccount, sourcePassword, amount):
        if PasswordSecurity.hash(sourcePassword, self.__saltKey) == self.__password:
            if self.__balance - amount >= 0:
                self.__subtract(amount)
                targetAccount.__add(amount)
            else:
                raise ValueError("Amount being attempted to transfer is greater than source account balance")
        else:
            raise Breach("Transfer attempted with incorrect password")

    # Calculating interest on an account given the interest rate
    def interest(self):
        if self.__isCompoundInterest:
            self.__balance *= 1+(self.__interestRate/100)
        else:
            moneyToAdd = (self.__lastBalanceWithoutInterest*(1+(self.__interestRate/100)) - self.__lastBalanceWithoutInterest)
            self.__balance += moneyToAdd

    # Initiate a new loan
    def loan(self, key, amount):
        if PasswordSecurity.hash(key, self.__saltKey) == self.__password:
            try :
                Loan(self,amount,key)
                self.loan_id+=1
            except LoanDenied:
                print("Loan denied")
        else:
            raise Breach("Loan attempted without key")

    # Pay a loan
    def payLoan(self, key, amount, fromBalance):
        if PasswordSecurity.hash(key, self.__saltKey) == self.__password:
            if fromBalance:
                self.__debt -= amount
                self.__balance -= amount
                self.__lastBalanceWithoutInterest = self.__balance
            else:
                self.__debt -= amount

    def netWorth(self):
        return self.__balance - self.__debt

    def add_debt(self,key,amount):
        if PasswordSecurity.hash(key, self.__saltKey) == self.__password:
            self.__debt += amount
        else:
            raise Breach("Loan attempted without key")