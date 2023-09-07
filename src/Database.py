import psycopg2
from Error import Error



# Database class
class Database():

    # constructor
    def __init__(self):
        self.__connector = None
        self.__cursor = None

    # connectToDatabase method that connect to database or open that
    def connectToDatabase(self):
        try:
            # connect to database
            self.__connector = psycopg2.connect(
                                   database="<database-name>",
                                   user="postgres",
                                   password="<postgresql-password>",
                                   host="127.0.0.1",
                                   port="5432"
                               )

            # create a cursor and create a table if it does not exist
            self.__cursor = self.__connector.cursor()

            # create table if it not exists
            self.__cursor.execute(
                """CREATE TABLE IF NOT EXISTS Account(
                Username      TEXT,
                Email         TEXT,
                Password      TEXT,
                Favorite_Club TEXT);"""
            )

            # save changes
            self.__connector.commit()

        except:
            obj = Error()
            obj.showError()

    # insert method that add new data (username, email, password, favorite club) to database
    def insert(self, username, email, password, favoriteClub):
        try:
            # create a tuple with the data
            userData = (username, email, password, favoriteClub)

            # insert data of the user operation
            self.__cursor.execute(
                """INSERT INTO Account(Username, Email, Password, Favorite_Club)
                VALUES(%s, %s, %s, %s)""", userData
            )

            # save changes
            self.__connector.commit()

            # close
            self.__close()

        except:
            obj = Error()
            obj.showError()

    # select method that select all usernames and emails and passwords from database
    def select(self):
        try:
            # select data from database (usernames and emails and passwords)
            self.__cursor.execute("SELECT * FROM Account")
            usersData = self.__cursor.fetchall()

            # close
            self.__close()

            return usersData

        except:
            obj = Error()
            obj.showError()

    # specialSelect method that select the desired user data from database
    def specialSelect(self, username):
        try:
            # create a tuple with the username
            username = (username, )

            # select the password from database
            self.__cursor.execute("SELECT * FROM Account WHERE Username = %s", username)
            userData = self.__cursor.fetchall()

            # close
            self.__close()

            return userData

        except:
            obj = Error()
            obj.showError()

    # updatePassword method that update the password of the user
    def updatePassword(self, username, newPassword):
        try:
            # create a tuple with the data
            data = (newPassword, username)

            # update password of the user operation
            self.__cursor.execute("UPDATE Account SET Password = %s WHERE Username = %s", data)

            # save changes
            self.__connector.commit()

            # close
            self.__close()

        except:
            obj = Error()
            obj.showError()

    # deleteAccount method that delete account of the user (remove user data from database)
    def deleteAccount(self, username):
        try:
            # create a tuple with the username
            username = (username, )

            # delete data of the from database
            self.__cursor.execute("DELETE FROM Account WHERE Username = %s", username)

            # save changes
            self.__connector.commit()

            # close
            self.__close()

        except:
            obj = Error()
            obj.showError()

    # close method that close the database cursor and connector
    def __close(self):
        try:
            self.__cursor.close()
            self.__connector.close()
        except:
            obj = Error()
            obj.showError()