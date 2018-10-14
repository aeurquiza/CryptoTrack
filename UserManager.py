import os
import base64
import mysql.connector
import User

def encode( password ):
	return base64.b64encode(password)

def decode( password ):
	return base64.b64decode(password)

class UserManager():
	INSERT_NEW_USER_QUERY = "INSERT INTO users (username, encryptedpw, email) VALUES"
	USER_MEMBERSHIP_QUERY = "SELECT 1 FROM users WHERE"
	GET_USER_QUERY = "SELECT * FROM users WHERE username"

	def __init__(self):
		self.dir_path = os.path.dirname(os.path.realpath(__file__))
		self.cnx = mysql.connector.connect(user = 'root', password = decode('YWV1cnF1aXph'), host = 'localhost', database = 'cryptoapp' )
		self.cursor = self.cnx.cursor( dictionary = True )
		self.currentUser = None
		self.loggedIn = False

	def addNewUser(self, username, password, email):
		if self.validNewUser(username, email):
			query = "{insert_new_user} ('{f_username}', '{f_password}', '{f_email}')".format( insert_new_user = self.INSERT_NEW_USER_QUERY,
													 f_username = username, f_password = encode(password), f_email = email)
			self.cursor.execute(query)
			self.__commit_query()

	def validNewUser(self, username, email):
		return not self.userExists(username) and not self.emailExists(email)

	def userExists(self, username):
		return self.exists('username',username)

	def emailExists(self, email):
		return self.exists('email',email)

	def exists(self, keyword, compare):
		query = "{if_user_exists} {f_keyword} = '{f_compare}'".format( if_user_exists = self.USER_MEMBERSHIP_QUERY,
														 f_keyword = keyword, f_compare = compare )
		self.cursor.execute(query)
		if self.cursor.fetchone() == None:
			return False
		return True

	def validateUser(self, username, password):
		query = "{get_user} = '{f_username}'".format( get_user = self.GET_USER_QUERY,
													 f_username = username )
		self.cursor.execute(query) 
		user_data = self.cursor.fetchone()
		if user_data == None:
			return False
		pw = user_data['encryptedpw']
		if encode(password) == pw:
			self.__loadUser(user_data)
			self.loggedIn = True
			return True
		return False

	def __loadUser(self, user_data):
		self.currentUser = User.User( username = user_data['username'], userid = user_data['userid'], email = user_data['email'])

	def logout(self):
		del self.currentUser

	def userLoggedIn(self):
		return self.loggedIn

	def __commit_query(self):
		self.cnx.commit()