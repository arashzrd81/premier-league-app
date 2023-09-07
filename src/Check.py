from PyQt5.QtCore import QCoreApplication
from validate_email import validate_email
from Database import Database



# Check class
class Check():

    # constructor
    def __init__(self):
        self.translate = QCoreApplication.translate
        self.database = Database()
        self.database.connectToDatabase()
        self.quorum = 0

    # checkSignUp method that check the inputs data in Sign Up section
    def checkSignUp(self, label, inputUsername, inputEmail, inputPassword):

        # get the data of the users
        usersData = self.database.select()

        # check username
        if inputUsername == '':
            label[9].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            isDuplication = False
            numUsernameChars = 0
            for account in usersData:
                if account[0] == inputUsername:
                    label[9].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Sorry, The username is taken. Try another.</span></p></body></html>"))
                    isDuplication = True
                    break

            if not isDuplication:
                for char in inputUsername:
                    if (not 'A' <= char <= 'Z') and (not 'a' <= char <= 'z') and (not '0' <= char <= '9') and (char != '.') and (char != '_'):
                        if char == ' ':
                            label[9].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid username! Don't use space (maybe used space at end).</span></p></body></html>"))
                        else:
                            label[9].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid username! Just use A-Z, a-z, 0-9, '.' & '_'.</span></p></body></html>"))
                        break
                    else:
                        numUsernameChars += 1

            if numUsernameChars == len(inputUsername):
                label[9].clear()
                self.quorum += 1

        # check email
        if inputEmail == '':
            label[10].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            isDuplication = False
            for account in usersData:
                if account[1] == inputEmail + "@gmail.com":
                    label[10].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Sorry, An account has already been created with this email.</span></p></body></html>"))
                    isDuplication = True
                    break

            if not isDuplication:
                validity = validate_email(inputEmail + "@gmail.com", verify=True)
                if validity:
                    label[10].clear()
                    self.quorum += 1
                else:
                    label[10].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid email!</span></p></body></html>"))

        # check password
        if inputPassword == '':
            label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            numPasswordChars = 0
            for char in inputPassword:
                if char == ' ':
                    label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid password! Don't use space (maybe used space at end).</span></p></body></html>"))
                    break
                else:
                    numPasswordChars += 1

            if numPasswordChars == len(inputPassword):
                if 8 <= len(inputPassword) <= 16:
                    label[11].clear()
                    self.quorum += 1
                else:
                    label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Count of password must between 8-16 characters.</span></p></body></html>"))

        return self.quorum

    # checkSignIn method that check the inputs data in Sign In section
    def checkSignIn(self, label, inputUsername, inputPassword):

        # get the data of the users
        usersData = self.database.select()

        # define userPassword
        userPassword = None

        # check username
        if inputUsername == '':
            label[6].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            isExists = False
            for account in usersData:
                if account[0] == inputUsername:
                    label[6].clear()
                    userPassword = account[2]
                    isExists = True
                    self.quorum += 1
                    break

            if not isExists:
                label[6].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid username!</span></p></body></html>"))

        # check password
        if inputPassword == '':
            label[7].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            if userPassword == inputPassword:
                label[7].clear()
                self.quorum += 1
            else:
                label[7].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid password!</span></p></body></html>"))

        return self.quorum

    # checkChangePassword method that check the inputs data in change password section
    def checkChangePassword(self, username, label, currentPassword, newPassword, newPasswordAgain):

        # get the data of the users
        userData = self.database.specialSelect(username)
        userPassword = userData[0][2]

        # check current password
        if currentPassword == '':
            label[10].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            if userPassword == currentPassword:
                label[10].clear()
                self.quorum += 1
            else:
                label[10].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid password!</span></p></body></html>"))

        # check new password
        if newPassword == '':
            label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            if ' ' in newPassword:
                label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Invalid password! Don't use space.</span></p></body></html>"))
            else:
                if 8 <= len(newPassword) <= 16:
                    label[11].clear()
                    self.quorum += 1
                else:
                    label[11].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">Count of password must between 8-16 characters.</span></p></body></html>"))

        # check new password again
        if newPasswordAgain == '':
            label[12].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">You did not fill in the item!</span></p></body></html>"))
        else:
            if newPassword == newPasswordAgain:
                label[12].clear()
                self.quorum += 1
            else:
                label[12].setText(self.translate("Form", "<html><head/><body><p><span style=\" font-size:10pt; font-weight:600; color:#ff0000;\">The password does not match the new password!</span></p></body></html>"))

        return self.quorum