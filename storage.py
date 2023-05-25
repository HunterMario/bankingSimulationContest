import os
import pickle

os.chdir(r"C:\Users\hunte\Documents\CodeProjects\bankSimulation\objects")

class Storage:
    # Function to get all accounts from objects folder
    def get():
        accounts = []
        for accountObject in os.listdir(os.getcwd()):
            currentObject = open(accountObject, "rb")
            accounts.append(pickle.load(currentObject))
        return accounts

    def getSpecificAccount(idNumber):
        accountToGet = open((str(idNumber) + ".obj"), "rb")
        return pickle.load(accountToGet)

    # Function to create a new file representing an account. Use when an account is being created.
    def createNew(obj):
        newFile = open((str(obj.id) + ".obj"), "xb")
        pickle.dump(obj, newFile)
        newFile.close()

    def update(obj):
        fileToOverwrite = open((str(obj.id) + ".obj"), "wb")
        pickle.dump(obj, fileToOverwrite)
        fileToOverwrite.close()

    def deleteAccount(obj):
        os.remove((str(obj.id) + ".obj"))