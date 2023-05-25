class Breach(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "Breach Details: " + str(self.message)

class LoanDenied(Exception):
    def __init__(self):
        self.message = "Loan Denied"

    def __str__(self):
        return self.message