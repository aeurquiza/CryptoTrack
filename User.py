
class User():
	def __init__(self, username, userid, email):
		self.name = username
		self.userid = userid
		self.email = email


	def convertToJSON(self):
		json.dumps(getObject())

	def getUserId(self):
		return self.userid
		

