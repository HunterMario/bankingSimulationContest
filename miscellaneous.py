import hashlib
import secrets
import string

class Address:
    def __init__(self, streetNumber, streetName, city, state, zipCode):
        self.streetNumber = int(streetNumber)
        self.streetName = streetName
        self.city = city
        self.state = state
        self.zipCode = int(zipCode)

    def __str__(self):
        return str(self.streetNumber) + " " + self.streetName + ", " + self.city + ", " + self.state + ", " + str(self.zipCode)

class DateOfBirth:
    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return str(DateOfBirth.months[self.month-1]) + " " + str(self.day) + ", " + str(self.year)

class PasswordSecurity:
	def salt():
		return ''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(8))

	def hash(password, saltString):
		saltLength = len(saltString)
		if saltLength % 2 == 1:
			saltLength -= 1
		leadSalt = saltString[:(int((saltLength/2)-2))]
		trailSalt = saltString[int((saltLength/2)-1):]
		saltedPassword = leadSalt + password + trailSalt
		return hashlib.sha256(saltedPassword.encode()).hexdigest()