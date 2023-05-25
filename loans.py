from customExceptions import LoanDenied
from datetime import datetime

class Loan :
    def __init__(self,owner,amount,password,Compound = False,interest=5):
        self.owner = owner
        self.id = owner.loan_id
        self.__balance = amount
        self.__password = password
        now = datetime.now()
        self.name = str(now.strftime("%H:%M:%S"))

        if owner.credit*owner.balance < self.__balance :
            raise LoanDenied
        self.owner.loans[self.id]=self
        owner.add_debt(self.__password,amount)
        self.owner.deposit(password,amount)
        self.__isCompoundInterest=Compound
        self.__interest= interest
        self.__start=amount

    def interest(self):
        if self.__isCompoundInterest:
            self.__balance *= 1+(self.__interest/100)
        else:
            self.__balance +=self.__start * (1+(self.__interest/100))



    def balance(self):
        return self.__balance

    def pay(self,amount = 0,isBal=False):

            if isBal:
                self.owner.withdraw(self.__password,amount)
                self.__balance -=amount
            else:
                self.__balance-=amount
            if self.__balance <= 0 :
                self.owner.deposit(self.__password, -1*self.__balance)
                amount -= self.__balance*-1
                del self.owner.loans[self.id]
            self.owner.add_debt(self.__password,amount*-1)
    def __dir__(self):
        return [self.__balance]
    def __repr__(self):
        return (self.name+" - "+str(self.__balance))
#Addie = Account("Addision", "8", 5, 9, 2005, 2819, "Cookies", "Chicago", "Texas", 38902, True, 4)